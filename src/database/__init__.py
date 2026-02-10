"""Database layer for BLM Financial Report Analysis.

Provides SQLite-based data storage with fiscal period alignment
and data provenance tracking. Cloud sync via Supabase.

Imports are lazy so the web app (which only uses supabase_data.py)
doesn't crash when heavy CLI-only deps (sqlite3, etc.) are missing.
"""


def __getattr__(name: str):
    """Lazy import to avoid pulling in sqlite3 / heavy deps on Vercel."""
    _import_map = {
        "TelecomDatabase": ("src.database.db", "TelecomDatabase"),
        "PeriodConverter": ("src.database.period_utils", "PeriodConverter"),
        "PeriodInfo": ("src.database.period_utils", "PeriodInfo"),
        "get_converter": ("src.database.period_utils", "get_converter"),
        "OPERATOR_DIRECTORY": ("src.database.operator_directory", "OPERATOR_DIRECTORY"),
        "EARNINGS_CALENDAR": ("src.database.operator_directory", "EARNINGS_CALENDAR"),
        "get_operators_for_market": ("src.database.operator_directory", "get_operators_for_market"),
        "get_operator_info": ("src.database.operator_directory", "get_operator_info"),
        "BLMSupabaseClient": ("src.database.supabase_client", "BLMSupabaseClient"),
        "BLMCloudSync": ("src.database.supabase_sync", "BLMCloudSync"),
    }
    if name in _import_map:
        module_path, attr = _import_map[name]
        import importlib
        mod = importlib.import_module(module_path)
        return getattr(mod, attr)
    raise AttributeError(f"module 'src.database' has no attribute {name!r}")


__all__ = [
    "TelecomDatabase",
    "PeriodConverter",
    "PeriodInfo",
    "get_converter",
    "OPERATOR_DIRECTORY",
    "EARNINGS_CALENDAR",
    "get_operators_for_market",
    "get_operator_info",
    "BLMSupabaseClient",
    "BLMCloudSync",
]
