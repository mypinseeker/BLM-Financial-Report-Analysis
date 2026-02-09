"""Seed the database with internet-sourced data for Germany telecom market.

Data collected from public sources on 2026-02-09, covering:
1. Regulatory insights (BNetzA, EU digital strategy)
2. Earnings call Q&A highlights (Vodafone Q3 FY26, O2, 1&1)
3. Media/industry reports (M&A, network strategy, market dynamics)

Each entry includes source_url for traceability.
"""

import sys
from pathlib import Path

_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase


def seed_source_registry(db: TelecomDatabase):
    """Register all data sources used in this seed."""
    sources = [
        {
            "source_id": "vod_q3fy26_trading_update",
            "source_type": "earnings_report",
            "url": "https://reports.investors.vodafone.com/view/412789358/",
            "document_name": "Vodafone Q3 FY26 Trading Update",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2026-02-05",
        },
        {
            "source_id": "vod_q3fy26_earnings_call",
            "source_type": "earnings_call",
            "url": "https://fintool.com/app/research/companies/VOD/earnings/Q3%202026",
            "document_name": "Vodafone Q3 FY26 Earnings Call Q&A",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2026-02-05",
        },
        {
            "source_id": "bnetza_spectrum_2025",
            "source_type": "regulator",
            "url": "https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/EN/2025/20250324_frequenzen.html",
            "document_name": "BNetzA Spectrum Extension Decision",
            "publisher": "Bundesnetzagentur",
            "publication_date": "2025-03-24",
        },
        {
            "source_id": "bnetza_spectrum_decision_pdf",
            "source_type": "regulator",
            "url": "https://www.bundesnetzagentur.de/SharedDocs/Downloads/EN/Areas/Telecommunications/Companies/TelecomRegulation/FrequencyManagement/ElectronicCommunicationsServices/Decision2025.pdf",
            "document_name": "BNetzA Decision on Spectrum Extension (Full Text)",
            "publisher": "Bundesnetzagentur",
            "publication_date": "2025-03-24",
        },
        {
            "source_id": "eu_digital_germany",
            "source_type": "regulator",
            "url": "https://digital-strategy.ec.europa.eu/en/policies/digital-connectivity-germany",
            "document_name": "Digital Connectivity in Germany",
            "publisher": "European Commission",
            "publication_date": "2025-01-23",
        },
        {
            "source_id": "vod_altice_fibreco",
            "source_type": "press_release",
            "url": "https://www.vodafone.com/news/newsroom/corporate-and-financial/vodafone-altice-create-joint-venture-deploy-fibre-to-the-home-germany",
            "document_name": "Vodafone and Altice FibreCo JV Announcement",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2025-07-15",
        },
        {
            "source_id": "vod_skaylink_acquisition",
            "source_type": "press_release",
            "url": "https://www.vodafone.com/news/corporate-and-financial/vodafone-to-acquire-skaylink",
            "document_name": "Vodafone to Acquire Skaylink",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2025-10-30",
        },
        {
            "source_id": "vod_skaylink_completion",
            "source_type": "press_release",
            "url": "https://www.vodafone.com/news/newsroom/corporate-and-financial/vodafone-completes-the-acquisition-of-skaylink",
            "document_name": "Vodafone Completes Skaylink Acquisition",
            "publisher": "Vodafone Group Plc",
            "publication_date": "2025-12-16",
        },
        {
            "source_id": "o2_q1_2025",
            "source_type": "earnings_report",
            "url": "https://www.telefonica.de/news/press-releases-telefonica-germany/2025/05/quarterly-results-customer-growth-strengthens-o2-telefonicas-operating-performance-in-the-first-quarter-2025.html",
            "document_name": "O2 Telefonica Germany Q1 2025 Results",
            "publisher": "Telefonica Deutschland",
            "publication_date": "2025-05-08",
        },
        {
            "source_id": "o2_q2_2025",
            "source_type": "earnings_report",
            "url": "https://www.telefonica.de/news/press-releases-telefonica-germany/2025/07/quarterly-results-customer-growth-across-segments-confirms-o2-telefonicas-course-in-the-second-quarter.html",
            "document_name": "O2 Telefonica Germany Q2 2025 Results",
            "publisher": "Telefonica Deutschland",
            "publication_date": "2025-07-24",
        },
        {
            "source_id": "one_one_q3_2025",
            "source_type": "earnings_report",
            "url": "https://imagepool.1und1.ag/v2/download/berichte/2025-1u1AG-Q3_EN.pdf",
            "document_name": "1&1 AG Interim Statement Q3 2025",
            "publisher": "1&1 AG",
            "publication_date": "2025-11-12",
        },
        {
            "source_id": "one_one_openran_migration",
            "source_type": "news",
            "url": "https://www.lightreading.com/finance/germany-s-1-1-migrates-all-mobile-customers-to-open-ran-5g-network",
            "document_name": "1&1 Migrates All Customers to Open RAN 5G Network",
            "publisher": "Light Reading",
            "publication_date": "2025-12-20",
        },
        {
            "source_id": "dt_q3_2025",
            "source_type": "earnings_report",
            "url": "https://www.telekom.com/en/investor-relations/publications/financial-results/financial-results-2025",
            "document_name": "Deutsche Telekom Q3 2025 Financial Results",
            "publisher": "Deutsche Telekom AG",
            "publication_date": "2025-11-13",
        },
        {
            "source_id": "vatm_market_2025",
            "source_type": "analyst",
            "url": "https://www.vatm.de/wp-content/uploads/2025/06/VATM-Market-Analysis-Germany-2025.pdf",
            "document_name": "26th Telecommunications Market Analysis Germany 2025",
            "publisher": "VATM",
            "publication_date": "2025-06-15",
        },
        {
            "source_id": "vod_mdu_impact",
            "source_type": "news",
            "url": "https://www.broadbandtvnews.com/2024/05/14/vodafones-german-recovery-hit-by-end-to-mdu-tv-switch/",
            "document_name": "Vodafone German Recovery Hit by MDU TV Switching",
            "publisher": "Broadband TV News",
            "publication_date": "2024-05-14",
        },
        {
            "source_id": "vod_cable_restructure",
            "source_type": "news",
            "url": "https://www.broadbandtvnews.com/2025/09/01/vodafone-restructures-tv-frequencies-across-germany-to-boost-cable-performance/",
            "document_name": "Vodafone Restructures TV Frequencies Across Germany",
            "publisher": "Broadband TV News",
            "publication_date": "2025-09-01",
        },
        {
            "source_id": "birdbird_spectrum_analysis",
            "source_type": "analyst",
            "url": "https://www.twobirds.com/en/insights/2025/german-bundesnetzagentur-provides-decision-to-extend-mobile-spectrum-subject-to-conditions",
            "document_name": "BNetzA Spectrum Extension Legal Analysis",
            "publisher": "Bird & Bird LLP",
            "publication_date": "2025-04-02",
        },
        {
            "source_id": "dt_targets_vodafone_fiber",
            "source_type": "news",
            "url": "https://www.telcotitans.com/deutsche-telekomwatch/germany-dt-targets-vodafone-as-it-reboots-fibre-tactics/9904.article",
            "document_name": "DT Targets Vodafone as It Reboots Fibre Tactics",
            "publisher": "TelcoTitans",
            "publication_date": "2025-08-15",
        },
    ]

    count = 0
    for src in sources:
        sql = """
            INSERT INTO source_registry (source_id, source_type, url, document_name, publisher, publication_date)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_id) DO UPDATE SET
                source_type = excluded.source_type,
                url = excluded.url,
                document_name = excluded.document_name,
                publisher = excluded.publisher,
                publication_date = excluded.publication_date
        """
        db.conn.execute(sql, (
            src["source_id"], src["source_type"], src["url"],
            src["document_name"], src["publisher"], src["publication_date"],
        ))
        count += 1

    db.conn.commit()
    print(f"  Registered {count} data sources")


def seed_intelligence_events(db: TelecomDatabase):
    """Insert intelligence events from internet research."""
    events = [
        # ── Regulatory / BNetzA ──
        {
            "operator_id": None,
            "market": "germany",
            "event_date": "2025-03-24",
            "category": "regulatory",
            "title": "BNetzA extends 800/1800/2600 MHz spectrum by 5 years",
            "description": (
                "BNetzA决定将800MHz、1800MHz、2600MHz频谱使用权延期5年（原2025年底到期）。"
                "附加条件：2030年99.5%国土面积≥50Mbps覆盖；2029年各州人口稀疏市镇99%家庭≥100Mbps。"
                "三家运营商须向MVNO/服务提供商协商频谱使用。"
                "特别要求：三家须向1&1提供800MHz 2×5MHz共用；O2须继续出租2600MHz 2×10MHz给1&1。"
                "预计2029年重新拍卖。"
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/EN/2025/20250324_frequenzen.html",
            "notes": "对DT/VF/O2利好（免拍卖费用），对1&1不利（无直接频谱延期）但获得共用权利",
        },
        {
            "operator_id": None,
            "market": "germany",
            "event_date": "2025-01-23",
            "category": "regulatory",
            "title": "German government launches €1.2B Gigabit Funding Programme 2025",
            "description": (
                "德国联邦数字化与交通部启动2025年千兆资助计划，拨款€12亿用于光纤基础设施建设。"
                "目标：2025年50%家庭FTTH/FTTB覆盖，2030年100%光纤覆盖。"
                "光纤连接数同比增长超20%。"
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://digital-strategy.ec.europa.eu/en/policies/digital-connectivity-germany",
            "notes": "对所有运营商利好，Vodafone通过Altice FibreCo合资可获取补贴",
        },
        {
            "operator_id": None,
            "market": "germany",
            "event_date": "2024-07-01",
            "category": "regulatory",
            "title": "Nebenkostenprivileg (MDU cable TV bundling) abolished",
            "description": (
                "自2024年7月1日起，房东不得再将有线电视费用计入物业附加费(Nebenkostenprivileg)。"
                "Vodafone受影响最大：原850万MDU用户，保留率约50%（~400万留存）。"
                "固网服务收入H1 FY25下降5.9%。到Q3 FY26固网降幅收窄至-1.1%，逆风减弱中。"
            ),
            "impact_type": "negative",
            "severity": "high",
            "source_url": "https://www.broadbandtvnews.com/2024/05/14/vodafones-german-recovery-hit-by-end-to-mdu-tv-switch/",
            "notes": "Vodafone特有风险（critical级），DT/O2影响小。Q3 FY26基数效应开始消退",
        },
        # ── Vodafone Strategic Events ──
        {
            "operator_id": "vodafone_germany",
            "market": "germany",
            "event_date": "2025-12-16",
            "category": "competitive",
            "title": "Vodafone completes Skaylink acquisition for €175M",
            "description": (
                "Vodafone完成对Skaylink的收购（€1.75亿，EV/EBITDA 7.0x），"
                "获得500+云和安全专家。Skaylink擅长AWS/Azure部署与迁移、AI解决方案。"
                "新任B2B负责人Hagen Rickmann目标：5年增加€10亿企业收入。"
                "这是Vodafone Business从连接型收入向数字化服务转型的关键一步。"
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://www.vodafone.com/news/newsroom/corporate-and-financial/vodafone-completes-the-acquisition-of-skaylink",
            "notes": "EV/EBITDA 7.0x，合理估值。关键看整合速度和交叉销售效果",
        },
        {
            "operator_id": "vodafone_germany",
            "market": "germany",
            "event_date": "2025-07-15",
            "category": "technology",
            "title": "Vodafone-Altice FibreCo JV: FTTH to 7M homes in 6 years",
            "description": (
                "Vodafone与Altice合资成立FibreCo，6年内为700万家庭部署FTTH。"
                "80%在Vodafone现有Cable覆盖区升级，20%新区域扩展。"
                "同步推进Cable升级：node splitting + DOCSIS 3.1 high-split（3Gbps）→ DOCSIS 4.0（10Gbps）。"
                "这是Vodafone从Cable向Fiber转型的核心战略举措。"
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://www.vodafone.com/news/newsroom/corporate-and-financial/vodafone-altice-create-joint-venture-deploy-fibre-to-the-home-germany",
            "notes": "解决了Vodafone光纤自有率低的核心问题。关键风险：执行速度和资本需求",
        },
        {
            "operator_id": "vodafone_germany",
            "market": "germany",
            "event_date": "2025-09-01",
            "category": "technology",
            "title": "Vodafone restructures cable TV frequencies nationwide",
            "description": (
                "Vodafone开始在全国Cable网络重组频率，创建统一频谱并释放宽带容量。"
                "技术升级覆盖400+城市、860万TV连接，预计2026年中完成。"
                "目标：为更快的宽带速度释放频谱资源。"
            ),
            "impact_type": "positive",
            "severity": "medium",
            "source_url": "https://www.broadbandtvnews.com/2025/09/01/vodafone-restructures-tv-frequencies-across-germany-to-boost-cable-performance/",
            "notes": "频率重组是Cable升级的前置条件，为DOCSIS 4.0铺路",
        },
        {
            "operator_id": "vodafone_germany",
            "market": "germany",
            "event_date": "2026-02-05",
            "category": "competitive",
            "title": "Vodafone completes 1&1 customer migration: 12M users on network",
            "description": (
                "Vodafone成功完成1&1客户迁移，1200万1&1客户已使用Vodafone全国5G网络。"
                "这是欧洲电信史上规模最大的客户迁移之一。"
                "批发收入贡献预计Q4 FY26达到完整运行率(full run-rate)。"
                "网络测试结果持续改善，迁移未影响网络质量。"
            ),
            "impact_type": "positive",
            "severity": "high",
            "source_url": "https://reports.investors.vodafone.com/view/412789358/",
            "notes": "批发收入是FY26最确定的增长引擎，但长期1&1自建网会分流",
        },
        # ── 1&1 Events ──
        {
            "operator_id": "one_and_one",
            "market": "germany",
            "event_date": "2025-12-31",
            "category": "new_entrant",
            "title": "1&1 completes OpenRAN migration, reaches 25% own network coverage",
            "description": (
                "1&1全部移动用户已迁移至自有OpenRAN 5G网络（欧洲首个）。"
                "自有基站约1,500个运营中，约4,500个在建。"
                "达到25%人口覆盖的监管截止日目标。"
                "Q3 2025移动净增+4万（H1因迁移影响基本持平）。"
                "9个月CAPEX €2.287亿主要用于建网。"
            ),
            "impact_type": "neutral",
            "severity": "high",
            "source_url": "https://www.lightreading.com/finance/germany-s-1-1-migrates-all-mobile-customers-to-open-ran-5g-network",
            "notes": "对Vodafone：短期利好（批发收入），长期威胁（流量将逐步减少）。OpenRAN先驱地位值得关注",
        },
        # ── Deutsche Telekom Events ──
        {
            "operator_id": "deutsche_telekom",
            "market": "germany",
            "event_date": "2025-11-13",
            "category": "competitive",
            "title": "Deutsche Telekom Q3 2025: revenue +1.5%, net profit +14.3%",
            "description": (
                "德电Q3 2025集团收入€289.35亿（+1.5% YoY），EBITDAaL利润率38.2%。"
                "净利润增长14.3%至€26.7亿。YTD自由现金流+6.8%至€161亿。"
                "德国区Q4展望：EBITDA增速>2%，受益于成本节约和工资/能源压力缓解。"
                "Q4 2025完整财报定于2026年2月26日发布。"
            ),
            "impact_type": "negative",
            "severity": "medium",
            "source_url": "https://www.telekom.com/en/investor-relations/publications/financial-results/financial-results-2025",
            "notes": "对Vodafone负面：德电持续拉大领先优势。DT的规模效应和运营纪律是标杆",
        },
        {
            "operator_id": "deutsche_telekom",
            "market": "germany",
            "event_date": "2025-08-15",
            "category": "competitive",
            "title": "DT reboots fibre tactics, targets Vodafone cable footprint",
            "description": (
                "德电调整光纤策略，开始在Vodafone Cable覆盖区域积极部署FTTH，"
                "直接与Vodafone的Cable+Fiber混合网络竞争。"
                "这是DT利用光纤先发优势抢夺Vodafone固网用户的进攻性策略。"
            ),
            "impact_type": "negative",
            "severity": "high",
            "source_url": "https://www.telcotitans.com/deutsche-telekomwatch/germany-dt-targets-vodafone-as-it-reboots-fibre-tactics/9904.article",
            "notes": "对Vodafone威胁严重：Cable用户可能被DT的纯光纤方案吸引",
        },
        # ── O2 / Telefónica Events ──
        {
            "operator_id": "telefonica_o2",
            "market": "germany",
            "event_date": "2025-07-24",
            "category": "competitive",
            "title": "O2 Germany Q2 2025: revenue -2.4% but IoT +47%, users growing",
            "description": (
                "O2 Q2 2025总收入下降2.4%（移动服务收入-3.4%），"
                "但用户增长强劲：Q2合同客户+18.4万。"
                "IoT连接增长47% YoY（Q2新增17.7万），是最大亮点。"
                "5G覆盖98%领先全行业。EBITDA利润率约30.6%稳定。"
            ),
            "impact_type": "neutral",
            "severity": "medium",
            "source_url": "https://www.telefonica.de/news/press-releases-telefonica-germany/2025/07/quarterly-results-customer-growth-across-segments-confirms-o2-telefonicas-course-in-the-second-quarter.html",
            "notes": "O2在IoT和用户增长方面表现出色，但收入承压。5G 98%覆盖对Vodafone形成网络压力",
        },
        # ── Market-level Events ──
        {
            "operator_id": None,
            "market": "germany",
            "event_date": "2025-06-15",
            "category": "economic",
            "title": "German telecom market reaches $86B, CAGR 5.53% to 2030",
            "description": (
                "VATM第26次市场分析报告：德国电信市场2025年规模$860亿（约€790亿年度），"
                "预计至2030年达$1,126亿，CAGR 5.53%。"
                "市场有150+服务提供商，竞争激烈。ARPU行业平均下降约4%。"
                "移动数据服务收入CAGR 9.5%，5G套餐是主要增长引擎。"
                "光纤连接数增长超20%，97%家庭有宽带覆盖。"
            ),
            "impact_type": "neutral",
            "severity": "medium",
            "source_url": "https://www.vatm.de/wp-content/uploads/2025/06/VATM-Market-Analysis-Germany-2025.pdf",
            "notes": "市场增长主要来自数据/5G/光纤，传统语音/SMS持续萎缩",
        },
    ]

    count = 0
    for event in events:
        db.upsert_intelligence(event)
        count += 1

    print(f"  Inserted {count} intelligence events")


def seed_earnings_call_highlights(db: TelecomDatabase):
    """Insert earnings call Q&A highlights."""
    highlights = [
        # ── Vodafone Q3 FY26 Earnings Call (2026-02-05) ──
        {
            "segment": "germany",
            "highlight_type": "guidance",
            "content": (
                "德国EBITDA：H2表现优于H1，但FY26不会回到正增长。"
                "关键顺风因素：(1) MDU同比基数效应Q3开始消退；"
                "(2) 1&1批发收入Q4达到完整运行率(full run-rate)；"
                "(3) MVNO基数效应。"
                "预计FY27才能真正实现EBITDA正增长。"
            ),
            "speaker": "Management",
            "source_url": "https://fintool.com/app/research/companies/VOD/earnings/Q3%202026",
            "notes": "分析师最关注的问题。投资者对德国恢复速度有顾虑",
        },
        {
            "segment": "germany_broadband",
            "highlight_type": "explanation",
            "content": (
                "宽带定价策略：2026年1月再次提价，采用'more-for-more'策略。"
                "固网消费者收入已企稳。新客宽带ARPU创三年新高（+21% YoY）。"
                "预计Q4总量趋势相似，但价值方程在发挥作用。"
                "2025年3月至10月间的零售定价行动正在支撑ARPU趋势。"
            ),
            "speaker": "Management",
            "source_url": "https://reports.investors.vodafone.com/view/412789358/",
            "notes": "'价值经营'策略在宽带端见效，是核心积极信号",
        },
        {
            "segment": "germany_mobile",
            "highlight_type": "explanation",
            "content": (
                "移动服务收入Q3增长2.8%（Q2: 3.8%），增速放缓。"
                "原因：批发收入增长被ARPU压力和服务提供商付款节奏部分抵消。"
                "1&1迁移完成后网络测试结果持续改善——1200万用户迁移是欧洲电信史上最大迁移之一。"
                "消费者合同客户净增42,000（Q2仅+1,000），消费者势头改善。"
            ),
            "speaker": "Management",
            "source_url": "https://reports.investors.vodafone.com/view/412789358/",
            "notes": "移动ARPU压力是隐忧。消费者合同净增恢复是积极信号",
        },
        {
            "segment": "germany_b2b",
            "highlight_type": "explanation",
            "content": (
                "Vodafone Business德国服务收入Q3下降1.8%（Q2: -1.6%），降幅扩大。"
                "原因：移动合同续约时ARPU下压 + 核心连接业务持续承压。"
                "亮点：数字服务需求强劲。Skaylink收购（2025年12月完成）"
                "预计将加速云、安全和托管服务增长。"
                "新任B2B负责人Hagen Rickmann的5年€10亿增长目标是关键战略承诺。"
            ),
            "speaker": "Management",
            "source_url": "https://reports.investors.vodafone.com/view/412789358/",
            "notes": "B2B是战略重点但短期仍在下滑，Skaylink是转折点",
        },
        {
            "segment": "group",
            "highlight_type": "guidance",
            "content": (
                "集团FY26指引重申上限：EBITDAaL €113-116亿，自由现金流€24-26亿。"
                "YTD EBITDAaL增长5.3%至€85亿，符合预期。"
                "集团服务收入Q3增长5.4%。"
                "2025年11月宣布FY26股息每股增长2.5%，反映中期自由现金流增长信心。"
            ),
            "speaker": "Management",
            "source_url": "https://www.stocktitan.net/sec-filings/VOD/6-k-vodafone-group-public-ltd-co-current-report-foreign-issuer-17b0d1c9489d.html",
            "notes": "集团层面健康，德国是改善最慢的市场",
        },
    ]

    count = 0
    for h in highlights:
        db.upsert_earnings_highlight("vodafone_germany", "CQ4_2025", h)
        count += 1

    print(f"  Inserted {count} earnings call highlights")


def seed_updated_macro(db: TelecomDatabase):
    """Update macro environment data with internet-sourced details.

    Reads existing data first to avoid overwriting fields we don't update.
    """
    # Read existing macro data for CQ4_2025
    row = db.conn.execute(
        "SELECT * FROM macro_environment WHERE country = ? AND calendar_quarter = ?",
        ("Germany", "CQ4_2025"),
    ).fetchone()

    existing = dict(row) if row else {}

    # Merge: only update fields we have new data for
    macro_update = {
        "gdp_growth_pct": existing.get("gdp_growth_pct"),
        "inflation_pct": existing.get("inflation_pct"),
        "unemployment_pct": existing.get("unemployment_pct"),
        "five_g_adoption_pct": existing.get("five_g_adoption_pct"),
        "fiber_penetration_pct": existing.get("fiber_penetration_pct"),
        "energy_cost_index": existing.get("energy_cost_index"),
        "consumer_confidence_index": existing.get("consumer_confidence_index"),
        # New/updated fields from internet research
        "telecom_market_size_eur_b": 79.0,  # $86B ≈ €79B (annual)
        "telecom_growth_pct": 5.53,  # CAGR 2025-2030
        "regulatory_environment": (
            "BNetzA: 800/1800/2600MHz频谱延期5年(2025.03决定)；"
            "覆盖义务2030年99.5%面积≥50Mbps；"
            "€12亿千兆资助计划(2025.01)；"
            "Nebenkostenprivileg 2024.07取消(MDU TV法规变更)；"
            "光纤目标2025年50%/2030年100% FTTH覆盖"
        ),
        "digital_strategy": (
            "Gigabit Strategy: FTTH/FTTB 50% by 2025, 100% by 2030; "
            "€1.2B Gigabit Funding Programme 2025; "
            "Fiber connections +20% YoY; "
            "5G coverage obligation: 99.5% area by 2030"
        ),
        "source_url": "https://www.bundesnetzagentur.de/SharedDocs/Pressemitteilungen/EN/2025/20250324_frequenzen.html",
        "notes": (
            "Sources: BNetzA spectrum decision (2025-03-24), "
            "EU Digital Connectivity Germany, "
            "VATM Market Analysis 2025"
        ),
    }

    db.upsert_macro("Germany", "CQ4_2025", macro_update)
    print(f"  Updated macro environment for CQ4_2025 with internet data")


def seed_internet_data(db: TelecomDatabase):
    """Run the complete internet data seed process."""
    print("\n=== Seeding Internet-Sourced Data ===")

    print("Step 1/4: Registering data sources...")
    seed_source_registry(db)

    print("Step 2/4: Inserting intelligence events (regulatory/media/strategic)...")
    seed_intelligence_events(db)

    print("Step 3/4: Inserting earnings call Q&A highlights...")
    seed_earnings_call_highlights(db)

    print("Step 4/4: Updating macro environment data...")
    seed_updated_macro(db)

    print("=== Internet data seed complete! ===\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Seed internet-sourced data")
    parser.add_argument(
        "--db-path", default="data/telecom.db",
        help="Path to SQLite database (default: data/telecom.db)",
    )
    args = parser.parse_args()

    db = TelecomDatabase(args.db_path)
    db.init()
    seed_internet_data(db)
    db.close()
