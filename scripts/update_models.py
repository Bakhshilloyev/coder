#!/usr/bin/env python3
"""Fetch the latest model list for a provider and write it to configs/models.json.

Usage:
    python scripts/update_models.py --provider groq --api-key $GROQ_API_KEY
"""
import argparse
import json
import os
import urllib.request


def fetch_groq_models(api_key: str) -> list:
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    return [m["id"] for m in data.get("data", [])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", default="groq")
    ap.add_argument("--api-key", default=None)
    args = ap.parse_args()

    key = args.api_key or os.environ.get("GROQ_API_KEY")
    if not key:
        print("No API key provided; writing placeholder entry only.")
        models = {}
    elif args.provider == "groq":
        ids = fetch_groq_models(key)
        models = {i: {"provider": "groq", "best_for": ["fast inference"]} for i in ids}
    else:
        print(f"Provider {args.provider} not supported by this script yet.")
        return

    path = os.path.join("configs", "models.json")
    existing = json.load(open(path)) if os.path.exists(path) else {}
    existing.update(models)
    with open(path, "w") as f:
        json.dump(existing, f, indent=2)
    print(f"Wrote {len(existing)} models to {path}")


if __name__ == "__main__":
    main()
