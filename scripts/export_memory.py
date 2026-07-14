#!/usr/bin/env python3
"""Export stored long-term memory to a JSON file for backup/portability."""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from agent.memory.sqlite_store import SQLiteStore  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default="data/memory/agent.db")
    ap.add_argument("--out", default="data/memory/export.json")
    args = ap.parse_args()

    store = SQLiteStore(args.db)
    data = {
        "facts": store.all(),
        "events": store.events(limit=1000),
    }
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Exported {len(data['facts'])} facts to {args.out}")


if __name__ == "__main__":
    main()
