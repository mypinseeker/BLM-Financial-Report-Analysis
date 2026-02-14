"""AnalysisRunnerService — orchestrates the full analysis pipeline.

Pipeline: Job Created -> Data Pull -> Engine Run -> Output Generation -> Upload -> Job Complete

Uses the Pull-to-SQLite strategy: fetches Supabase data into a temp SQLite DB
via BLMCloudSync.pull_all(), then runs BLMAnalysisEngine against it as-is.
"""

from __future__ import annotations

import json
import tempfile
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional

from src.web.services.supabase_data import SupabaseDataService


# Storage bucket for analysis outputs
BUCKET = "blm-outputs"


class AnalysisRunnerService:
    """Orchestrates single-market and group analysis jobs end-to-end."""

    def __init__(self, svc: SupabaseDataService):
        self.svc = svc

    # ==================================================================
    # Single-market analysis
    # ==================================================================

    def run_single(self, job_id: int) -> dict:
        """Execute a single-market analysis job end-to-end.

        Returns dict with status, output_count, and any error message.
        """
        job = self.svc.get_analysis_job(job_id)
        if not job:
            return {"status": "failed", "error": f"Job #{job_id} not found"}

        market = job.get("market", "")
        operator = job.get("target_operator", "")
        period = job.get("analysis_period", "CQ4_2025")
        n_quarters = job.get("n_quarters", 8)

        self._update_job(job_id, {
            "status": "running",
            "progress": json.dumps({market: "running_pull"}),
            "started_at": datetime.utcnow().isoformat(),
        })

        tmp_dir = None
        try:
            # 1. Pull data from Supabase -> temp SQLite
            tmp_dir = tempfile.mkdtemp(prefix="blm_analysis_")
            db_path = str(Path(tmp_dir) / "analysis.db")
            db = self._pull_market_data(market, db_path)

            # 2. Run the analysis engine
            self._update_job(job_id, {
                "progress": json.dumps({market: "running_engine"}),
            })
            result = self._run_engine(db, operator, market, period, n_quarters,
                                      job_id=job_id)

            # 3. Generate output files
            self._update_job(job_id, {
                "progress": json.dumps({market: "running_output"}),
            })
            output_files = self._generate_outputs(result, market, operator, period, tmp_dir)

            # 4. Upload outputs to Supabase Storage + register
            self._update_job(job_id, {
                "progress": json.dumps({market: "uploading"}),
            })
            self._upload_outputs(output_files, market, operator, period)

            # 5. Mark complete
            self._update_job(job_id, {
                "status": "completed",
                "progress": json.dumps({market: "completed"}),
                "completed_at": datetime.utcnow().isoformat(),
            })

            db.close()
            return {
                "status": "completed",
                "output_count": len(output_files),
                "market": market,
                "operator": operator,
            }

        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            self._update_job(job_id, {
                "status": "failed",
                "progress": json.dumps({market: "failed"}),
                "error_message": error_msg[:500],
            })
            return {"status": "failed", "error": error_msg}
        finally:
            self._cleanup_temp(tmp_dir)

    # ==================================================================
    # Group analysis
    # ==================================================================

    def run_group(self, job_id: int) -> dict:
        """Execute a group analysis job — iterate markets + generate group summary.

        Returns dict with status, per-market results, and output counts.
        """
        job = self.svc.get_analysis_job(job_id)
        if not job:
            return {"status": "failed", "error": f"Job #{job_id} not found"}

        config = job.get("config", "{}")
        if isinstance(config, str):
            config = json.loads(config)

        group_id = job.get("group_id", "")
        period = job.get("analysis_period", "CQ4_2025")
        n_quarters = job.get("n_quarters", 8)
        selected_markets = config.get("selected_markets", [])

        progress = {m: "pending" for m in selected_markets}
        self._update_job(job_id, {
            "status": "running",
            "progress": json.dumps(progress),
            "started_at": datetime.utcnow().isoformat(),
        })

        # Resolve operators per market from group subsidiaries
        subs = self.svc.get_group_subsidiaries(group_id)
        market_operator_map = {s["market"]: s["operator_id"] for s in subs}

        market_results = {}
        total_outputs = 0

        # Run each market
        for market in selected_markets:
            operator = market_operator_map.get(market, "")
            if not operator:
                progress[market] = "failed"
                self._update_job(job_id, {"progress": json.dumps(progress)})
                continue

            progress[market] = "running"
            self._update_job(job_id, {"progress": json.dumps(progress)})

            tmp_dir = None
            try:
                tmp_dir = tempfile.mkdtemp(prefix=f"blm_{market}_")
                db_path = str(Path(tmp_dir) / "analysis.db")
                db = self._pull_market_data(market, db_path)

                progress[market] = "running_engine"
                self._update_job(job_id, {"progress": json.dumps(progress)})

                result = self._run_engine(db, operator, market, period, n_quarters,
                                          job_id=job_id)
                market_results[market] = result

                progress[market] = "running_output"
                self._update_job(job_id, {"progress": json.dumps(progress)})

                output_files = self._generate_outputs(result, market, operator, period, tmp_dir)
                self._upload_outputs(output_files, market, operator, period)
                total_outputs += len(output_files)

                progress[market] = "completed"
                self._update_job(job_id, {"progress": json.dumps(progress)})

                db.close()

            except Exception as e:
                progress[market] = "failed"
                self._update_job(job_id, {"progress": json.dumps(progress)})
                print(f"  [!] Market {market} failed: {e}")
                traceback.print_exc()
            finally:
                self._cleanup_temp(tmp_dir)

        # Generate group summary if we have results
        if market_results:
            try:
                from src.web.services.group_summary import GroupSummaryGenerator

                group_info = self.svc.get_operator_group(group_id) or {}
                summary_gen = GroupSummaryGenerator()
                summary = summary_gen.generate(market_results, group_info)

                # Upload group summary as JSON + TXT
                summary_files = self._generate_group_summary_outputs(
                    summary, group_id, period
                )
                self._upload_group_summary(summary_files, group_id, period)
                total_outputs += len(summary_files)
            except Exception as e:
                print(f"  [!] Group summary generation failed: {e}")
                traceback.print_exc()

        # Final status
        all_completed = all(v == "completed" for v in progress.values())
        any_completed = any(v == "completed" for v in progress.values())
        final_status = "completed" if all_completed else (
            "completed" if any_completed else "failed"
        )

        self._update_job(job_id, {
            "status": final_status,
            "progress": json.dumps(progress),
            "completed_at": datetime.utcnow().isoformat(),
        })

        return {
            "status": final_status,
            "markets": progress,
            "output_count": total_outputs,
        }

    # ==================================================================
    # Internal: data pull
    # ==================================================================

    def _pull_market_data(self, market: str, db_path: str):
        """Pull all Supabase data for a market into a local temp SQLite.

        Returns an initialized TelecomDatabase instance.
        """
        from src.database.db import TelecomDatabase
        from src.database.supabase_sync import BLMCloudSync

        db = TelecomDatabase(db_path)
        db.init()

        syncer = BLMCloudSync(local_db=db)
        print(f"  Pulling data for market '{market}' -> {db_path}")
        report = syncer.pull_all(market)
        total_rows = sum(report.tables.values())
        print(f"  Pulled {total_rows} rows across {len(report.tables)} tables")

        if report.errors:
            print(f"  Pull warnings: {report.errors}")

        return db

    # ==================================================================
    # Internal: engine execution
    # ==================================================================

    def _run_engine(self, db, operator: str, market: str,
                    period: str, n_quarters: int,
                    job_id: int = None):
        """Instantiate and run BLMAnalysisEngine. Returns FiveLooksResult."""
        from src.blm.engine import BLMAnalysisEngine

        print(f"  Running BLM Five Looks: {operator} in {market} ({period})")
        engine = BLMAnalysisEngine(
            db=db,
            target_operator=operator,
            market=market,
            target_period=period,
            n_quarters=n_quarters,
        )
        result = engine.run_five_looks()
        print(f"  Engine complete: {result.analysis_period}")

        # Persist provenance data if available
        if result.provenance and job_id is not None:
            try:
                stats = result.provenance.save_to_db(db, analysis_job_id=job_id)
                print(f"  Provenance saved: {stats['sources_saved']} sources, "
                      f"{stats['values_saved']} values")
            except Exception as e:
                print(f"  [!] Provenance save failed: {e}")

        return result

    # ==================================================================
    # Internal: output generation
    # ==================================================================

    def _generate_outputs(self, result, market: str, operator: str,
                          period: str, tmp_dir: str) -> list[dict]:
        """Generate all output files and return metadata dicts.

        Each dict: {type, file_name, file_path, content_type, size_bytes}
        """
        outputs = []
        output_dir = Path(tmp_dir) / "output"
        output_dir.mkdir(exist_ok=True)

        safe_op = operator.replace(" ", "_").lower()

        # 1. JSON (always)
        try:
            from src.output.json_exporter import BLMJsonExporter
            exporter = BLMJsonExporter()
            json_name = f"blm_{safe_op}_analysis_{period.lower()}.json"
            json_path = exporter.export(result, str(output_dir / json_name))
            outputs.append({
                "type": "json",
                "file_name": json_name,
                "file_path": json_path,
                "content_type": "application/json",
                "size_bytes": Path(json_path).stat().st_size,
            })
            print(f"    JSON: {json_name}")
        except Exception as e:
            print(f"    [!] JSON generation failed: {e}")

        # 2. TXT
        try:
            from src.output.txt_formatter import BLMTxtFormatter
            formatter = BLMTxtFormatter()
            txt_content = formatter.format(result)
            txt_name = f"blm_{safe_op}_analysis_{period.lower()}.txt"
            txt_path = output_dir / txt_name
            txt_path.write_text(txt_content, encoding="utf-8")
            outputs.append({
                "type": "txt",
                "file_name": txt_name,
                "file_path": str(txt_path),
                "content_type": "text/plain",
                "size_bytes": txt_path.stat().st_size,
            })
            print(f"    TXT: {txt_name}")
        except Exception as e:
            print(f"    [!] TXT generation failed: {e}")

        # 3. HTML
        try:
            from src.output.html_generator import BLMHtmlGenerator
            from src.output.ppt_styles import get_style
            style = get_style(operator)
            html_gen = BLMHtmlGenerator(style=style)
            html_name = f"blm_{safe_op}_analysis_{period.lower()}.html"
            html_path = html_gen.generate(result, str(output_dir / html_name))
            outputs.append({
                "type": "html",
                "file_name": html_name,
                "file_path": html_path,
                "content_type": "text/html",
                "size_bytes": Path(html_path).stat().st_size,
            })
            print(f"    HTML: {html_name}")
        except Exception as e:
            print(f"    [!] HTML generation failed: {e}")

        # 4. PPT (optional — needs python-pptx + matplotlib)
        try:
            from src.output.ppt_generator import BLMPPTGenerator
            from src.output.ppt_styles import get_style
            style = get_style(operator)
            ppt_gen = BLMPPTGenerator(
                style=style, operator_id=operator,
                output_dir=str(output_dir),
            )
            ppt_name = f"blm_{safe_op}_analysis_{period.lower()}.pptx"
            ppt_path = ppt_gen.generate(result, filename=ppt_name)
            outputs.append({
                "type": "pptx",
                "file_name": ppt_name,
                "file_path": ppt_path,
                "content_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
                "size_bytes": Path(ppt_path).stat().st_size,
            })
            print(f"    PPT: {ppt_name}")
        except ImportError:
            print("    [i] PPT skipped (python-pptx not installed)")
        except Exception as e:
            print(f"    [!] PPT generation failed: {e}")

        # 5. MD (Strategic Insight Report)
        try:
            from src.output.md_generator import BLMMdGenerator
            md_gen = BLMMdGenerator()
            md_name = f"blm_{safe_op}_analysis_{period.lower()}.md"
            md_content = md_gen.generate(result)
            md_path = output_dir / md_name
            md_path.write_text(md_content, encoding="utf-8")
            outputs.append({
                "type": "md",
                "file_name": md_name,
                "file_path": str(md_path),
                "content_type": "text/markdown",
                "size_bytes": md_path.stat().st_size,
            })
            print(f"    MD: {md_name}")
        except Exception as e:
            print(f"    [!] MD generation failed: {e}")

        return outputs

    def _generate_group_summary_outputs(self, summary: dict,
                                         group_id: str,
                                         period: str) -> list[dict]:
        """Generate JSON and TXT output files for the group summary."""
        import json as json_mod

        outputs = []
        tmp_dir = tempfile.mkdtemp(prefix="blm_group_")
        output_dir = Path(tmp_dir)

        # JSON
        json_name = f"blm_{group_id}_group_summary_{period.lower()}.json"
        json_path = output_dir / json_name
        json_path.write_text(
            json_mod.dumps(summary, indent=2, ensure_ascii=False, default=str),
            encoding="utf-8",
        )
        outputs.append({
            "type": "json",
            "file_name": json_name,
            "file_path": str(json_path),
            "content_type": "application/json",
            "size_bytes": json_path.stat().st_size,
        })

        # TXT
        txt_name = f"blm_{group_id}_group_summary_{period.lower()}.txt"
        txt_path = output_dir / txt_name
        txt_content = self._format_group_summary_txt(summary, group_id, period)
        txt_path.write_text(txt_content, encoding="utf-8")
        outputs.append({
            "type": "txt",
            "file_name": txt_name,
            "file_path": str(txt_path),
            "content_type": "text/plain",
            "size_bytes": txt_path.stat().st_size,
        })

        return outputs

    def _format_group_summary_txt(self, summary: dict, group_id: str,
                                   period: str) -> str:
        """Format group summary as plain text."""
        lines = []
        lines.append("=" * 80)
        lines.append(f"  BLM Group Analysis Summary: {group_id.upper()}")
        lines.append(f"  Period: {period}")
        lines.append(f"  Markets: {summary.get('market_count', 0)}")
        lines.append("=" * 80)

        # Revenue comparison
        rev = summary.get("revenue_comparison", {})
        if rev:
            lines.append("\n[Revenue Comparison]")
            for market, data in rev.items():
                rev_val = data.get("total_revenue", "N/A")
                growth = data.get("revenue_growth_pct", "N/A")
                lines.append(f"  {market:20s}  Revenue: {rev_val}  Growth: {growth}")

        # Subscriber comparison
        subs = summary.get("subscriber_comparison", {})
        if subs:
            lines.append("\n[Subscriber Comparison]")
            for market, data in subs.items():
                mobile = data.get("mobile_subs_k", "N/A")
                lines.append(f"  {market:20s}  Mobile Subs: {mobile}K")

        # Common opportunities
        opps = summary.get("common_opportunities", [])
        if opps:
            lines.append("\n[Common Opportunities (2+ markets)]")
            for opp in opps[:10]:
                lines.append(f"  -> {opp}")

        # Common threats
        threats = summary.get("common_threats", [])
        if threats:
            lines.append("\n[Common Threats (2+ markets)]")
            for threat in threats[:10]:
                lines.append(f"  !! {threat}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    # ==================================================================
    # Internal: upload
    # ==================================================================

    def _upload_outputs(self, output_files: list[dict], market: str,
                        operator: str, period: str) -> None:
        """Upload generated files to Supabase Storage + register in analysis_outputs."""
        self.svc.ensure_bucket(BUCKET)
        storage_prefix = f"{market}/{operator}/{period}"

        for out in output_files:
            try:
                file_data = Path(out["file_path"]).read_bytes()
                storage_path = f"{storage_prefix}/{out['file_name']}"

                # Upload to storage
                self.svc.upload_output_file(
                    BUCKET, storage_path, file_data, out["content_type"]
                )

                # Register in analysis_outputs table
                self.svc.register_analysis_output({
                    "market_id": market,
                    "operator_id": operator,
                    "analysis_period": period,
                    "output_type": out["type"],
                    "module_name": None,
                    "file_name": out["file_name"],
                    "storage_path": storage_path,
                    "file_size_bytes": out["size_bytes"],
                    "updated_at": datetime.utcnow().isoformat(),
                })
                print(f"    Uploaded: {storage_path}")
            except Exception as e:
                print(f"    [!] Upload failed for {out['file_name']}: {e}")

    def _upload_group_summary(self, output_files: list[dict],
                               group_id: str, period: str) -> None:
        """Upload group summary outputs."""
        self.svc.ensure_bucket(BUCKET)
        storage_prefix = f"groups/{group_id}/{period}"

        for out in output_files:
            try:
                file_data = Path(out["file_path"]).read_bytes()
                storage_path = f"{storage_prefix}/{out['file_name']}"

                self.svc.upload_output_file(
                    BUCKET, storage_path, file_data, out["content_type"]
                )

                self.svc.register_analysis_output({
                    "market_id": group_id,
                    "operator_id": group_id,
                    "analysis_period": period,
                    "output_type": f"group_{out['type']}",
                    "module_name": "group_summary",
                    "file_name": out["file_name"],
                    "storage_path": storage_path,
                    "file_size_bytes": out["size_bytes"],
                    "updated_at": datetime.utcnow().isoformat(),
                })
                print(f"    Uploaded group summary: {storage_path}")
            except Exception as e:
                print(f"    [!] Group summary upload failed: {e}")

    # ==================================================================
    # Internal: job update + cleanup
    # ==================================================================

    def _update_job(self, job_id: int, updates: dict) -> None:
        """Update analysis_jobs row."""
        self.svc.update_analysis_job(job_id, updates)

    @staticmethod
    def _cleanup_temp(tmp_dir: Optional[str]) -> None:
        """Remove temporary directory."""
        if tmp_dir:
            import shutil
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except Exception:
                pass
