#!/usr/bin/env python3
"""Print a concise summary of a JSON report produced by check_feeds.py."""
import argparse
import json
from collections import Counter
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", type=Path, help="JSON health report")
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    results = report.get("results", [])
    counts = Counter(item.get("health", "unknown") for item in results)
    print(f"Feed health report generated at {report.get('generated_at', 'unknown')}")
    print(f"Total: {len(results)} | " + " | ".join(f"{key}: {counts[key]}" for key in ("healthy", "degraded", "inconclusive", "broken")))
    for item in results:
        print(f"[{item.get('health', 'unknown')}] {item.get('id')} — {item.get('name')} — HTTP {item.get('http_status') or 'n/a'} — {item.get('feed_url')}")
        if item.get("error"):
            print(f"  {item['error']}")
        if item.get("recommended_action"):
            print(f"  Next: {item['recommended_action']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
