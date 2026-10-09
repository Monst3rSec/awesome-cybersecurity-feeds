#!/usr/bin/env python3
"""Generate the curated directory section of README.md deterministically."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.data_utils import load_dataset

START = "<!-- BEGIN GENERATED DIRECTORY -->"
END = "<!-- END GENERATED DIRECTORY -->"


def render_directory(data: dict) -> str:
    lines = [
        START,
        "## Directory",
        "",
        "Browse sources by category. Entries and descriptions are maintained in `security_feeds.yaml`.",
        "",
        "### Categories",
        "",
    ]
    categories = data["meta"]["categories"]
    for category in categories:
        lines.append(f"- [{category['name']}](#{category['id']}) — {category['description']}")
    lines.extend(["", "### Sources", ""])
    entities = data["entities"]
    for category in categories:
        cid = category["id"]
        lines.extend([f"<a id=\"{cid}\"></a>", f"#### {category['name']}", ""])
        matches = [entity for entity in entities if cid in entity["categories"]]
        if not matches:
            lines.extend(["_No sources listed yet._", ""])
            continue
        lines.extend([
            "| Publisher | Website | Feed | Format |",
            "| --- | --- | --- | --- |",
        ])
        for item in sorted(matches, key=lambda row: (row["name"].casefold(), row["id"])):
            website = item["website"]
            feed_url = item["feed"]["url"]
            publisher = item.get("publisher", item["name"])
            lines.append(f"| {publisher} | [{item['name']}]({website}) | [Feed]({feed_url}) | {item['feed']['format']} |")
        lines.append("")
    lines.extend([
        "For machine-readable fields, including IDs, provenance, verification dates, and notes, use the canonical [`security_feeds.yaml`](security_feeds.yaml) file.",
        END,
    ])
    return "\n".join(lines)


def update_readme(readme: Path, data: dict) -> bool:
    content = readme.read_text(encoding="utf-8")
    section = render_directory(data)
    if START in content and END in content:
        before, remainder = content.split(START, 1)
        _, after = remainder.split(END, 1)
        replacement = before.rstrip() + "\n\n" + section + after
    else:
        replacement = content.rstrip() + "\n\n" + section + "\n"
    if replacement != content:
        readme.write_text(replacement, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "security_feeds.yaml")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    args = parser.parse_args()
    update_readme(args.readme, load_dataset(args.data))
    print(f"Generated directory section in {args.readme}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
