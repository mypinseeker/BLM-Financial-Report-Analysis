"""Initialize and optionally seed the BLM telecom database.

Usage:
    python -m src.database.init_db                  # Create schema only
    python -m src.database.init_db --seed            # Create schema + seed Germany data
    python -m src.database.init_db --db-path custom.db --seed
"""

import argparse
import sys
from pathlib import Path

# Ensure project root is on path
_project_root = Path(__file__).resolve().parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.database.db import TelecomDatabase


def init_database(db_path: str = "data/telecom.db", seed: bool = False):
    """Create the database and optionally seed with Germany market data.

    Args:
        db_path: Path to SQLite database file
        seed: If True, run the Germany seed script after schema creation
    """
    print(f"Initializing database at: {db_path}")

    db = TelecomDatabase(db_path)
    db.init()
    print("Schema created successfully.")

    if seed:
        print()
        from src.database.seed_germany import seed_all
        db.close()
        seed_all(db_path)
    else:
        db.close()

    print(f"\nDatabase ready: {db_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize the BLM telecom database"
    )
    parser.add_argument(
        "--db-path", default="data/telecom.db",
        help="Path to SQLite database (default: data/telecom.db)"
    )
    parser.add_argument(
        "--seed", action="store_true",
        help="Seed with Germany market data after creation"
    )
    args = parser.parse_args()

    init_database(db_path=args.db_path, seed=args.seed)


if __name__ == "__main__":
    main()
