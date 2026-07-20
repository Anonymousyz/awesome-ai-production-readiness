#!/usr/bin/env python3
"""Export the curated README list as a deterministic machine-readable catalog."""
from __future__ import annotations

import argparse
from datetime import date
import hashlib
import json
from pathlib import Path
import re

RESOURCE_RE = re.compile(
    r"^- \[([^\]]+)\]\((https?://[^)]+)\)(?:\s*:\s*|\s+—\s+)(.+)$"
)
SECTION_TYPES = {
    "Evaluation and testing": "evaluation-framework",
    "Observability and monitoring": "observability-tool",
    "Guardrails and safety": "guardrail-tool",
    "Responsible AI and governance": "governance-resource",
    "Model/system documentation": "documentation-resource",
    "Human-centered AI": "human-centered-design-resource",
    "Security and risk frameworks": "security-resource",
    "RAG and agent production patterns": "application-framework",
    "Deployment and MLOps infrastructure": "deployment-tool",
    "Production readiness checklists": "readiness-checklist",
    "FDE and deployment workflow": "workflow-resource",
}
MARKERS = {
    "**Archived upstream**;": ("archived", True),
    "**Maintenance review**;": ("maintenance-review", False),
}


def normalize_url(url: str) -> str:
    return url.rstrip("/").lower()


def validated_date(value: str, label: str) -> date:
    if (
        not isinstance(value, str)
        or re.fullmatch(r"\d{4}-\d{2}-\d{2}", value) is None
    ):
        raise ValueError(f"{label} must be an ISO date (YYYY-MM-DD)")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{label} must be an ISO date (YYYY-MM-DD)") from exc
    if parsed > date.today():
        raise ValueError(f"{label} cannot be in the future")
    return parsed


def resource_status(description: str) -> tuple[str, bool, str]:
    for marker, (status, archived) in MARKERS.items():
        if description.startswith(marker):
            return status, archived, description[len(marker):].strip()
    return "active", False, description.strip()


def parse_resources(readme: Path, verified_at: str | None = None) -> list[dict]:
    if verified_at is not None:
        validated_date(verified_at, "verified_at")
    resources = []
    section = None
    seen = set()
    for raw in readme.read_text(encoding="utf-8").splitlines():
        if raw.startswith("## "):
            section = raw[3:].strip()
            continue
        match = RESOURCE_RE.match(raw.strip())
        if not match:
            continue
        if section not in SECTION_TYPES:
            raise ValueError(
                f"resource bullet under unregistered section {section!r}: {match.group(1)}"
            )
        name, url, description = match.groups()
        key = normalize_url(url)
        if key in seen:
            raise ValueError(f"duplicate resource URL: {url}")
        seen.add(key)
        status, archived, clean_description = resource_status(description)
        resources.append(
            {
                "name": name,
                "url": url,
                "canonical_url": url,
                "description": clean_description,
                "section": section,
                "type": SECTION_TYPES[section],
                "status": status,
                "archived": archived,
                "license": None,
                "last_verified": verified_at,
                "authoritative_source": url,
            }
        )
    return resources


def build_catalog(readme: Path, curated_at: str, verified_at: str | None = None) -> dict:
    curated_date = validated_date(curated_at, "curated_at")
    verified_date = validated_date(verified_at, "verified_at") if verified_at is not None else None
    if verified_date is not None and verified_date > curated_date:
        raise ValueError("verified_at cannot be later than curated_at")
    resources = parse_resources(readme, verified_at)
    serialized = json.dumps(resources, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {
        "schema_version": "2.0",
        "curated_at": curated_at,
        "catalog_sha256": hashlib.sha256(serialized.encode("utf-8")).hexdigest(),
        "count": len(resources),
        "resources": resources,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--output", default="data/resources.json")
    parser.add_argument(
        "--curated-at",
        required=True,
        help="Catalog-generation/review date (YYYY-MM-DD); does not imply every resource was checked",
    )
    parser.add_argument(
        "--verified-at",
        help="Optional date only when every exported resource was individually verified (YYYY-MM-DD)",
    )
    args = parser.parse_args(argv)
    payload = build_catalog(Path(args.readme), args.curated_at, args.verified_at)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Exported {payload['count']} resources to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
