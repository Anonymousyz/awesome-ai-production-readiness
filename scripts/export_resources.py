#!/usr/bin/env python3
"""Export Markdown resource bullets from README.md as a machine-readable catalog."""
from __future__ import annotations
import argparse
from datetime import date
import json
from pathlib import Path
import re

ENTRY = re.compile(r"^- \[([^]]+)\]\((https?://[^)]+)\)\s+[—-]\s+(.+)$")
HEADING = re.compile(r"^##\s+(.+?)\s*$")


def extract(readme: Path) -> list[dict[str, str]]:
    category = "Uncategorized"
    rows: list[dict[str, str]] = []
    seen: set[str] = set()
    for raw in readme.read_text(encoding="utf-8").splitlines():
        heading = HEADING.match(raw)
        if heading:
            category = heading.group(1)
            continue
        match = ENTRY.match(raw)
        if not match:
            continue
        name, url, description = match.groups()
        normalized = url.rstrip("/").lower()
        if normalized in seen:
            raise ValueError(f"duplicate resource URL in curated sections: {url}")
        seen.add(normalized)
        rows.append({"name": name, "url": url, "description": description, "category": category})
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--output", default="data/resources.json")
    parser.add_argument("--curated-at", default=date.today().isoformat())
    args = parser.parse_args(argv)
    readme = Path(args.readme)
    rows = extract(readme)
    payload = {"schema_version": 1, "curated_at": args.curated_at, "count": len(rows), "resources": rows}
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Exported {len(rows)} resources to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
