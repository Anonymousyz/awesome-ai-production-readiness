# Using the machine-readable catalog

`data/resources.json` is the canonical machine-readable export of this list. It is regenerated from `README.md` by `scripts/export_resources.py`, validated by the public JSON Schema, and checked in CI on every push, so downstream consumers can rely on its structure.

## Where to fetch it

| Need | URL |
|---|---|
| Latest catalog (moves with `main`) | `https://raw.githubusercontent.com/Anonymousyz/awesome-ai-production-readiness/main/data/resources.json` |
| Version-pinned catalog | `https://raw.githubusercontent.com/Anonymousyz/awesome-ai-production-readiness/v0.3.4/data/resources.json` |
| JSON Schema (Draft 2020-12) | `https://raw.githubusercontent.com/Anonymousyz/awesome-ai-production-readiness/v0.3.4/data/resources.schema.json` |
| Release asset with checksums | the `-resources.json` file attached to each [GitHub release](https://github.com/Anonymousyz/awesome-ai-production-readiness/releases) |

Pin a tag or use the checksummed release asset for anything reproducible; `main` may change between curation reviews.

## Record shape

Each entry in `resources` carries: `name`, `url`, `canonical_url`, `description`, `section`, `type`, `status` (`active` / `maintenance-review` / `archived`), `archived` (boolean, always consistent with `status`), `license` (currently `null`), `last_verified` (`null` unless every item was individually checked), and `authoritative_source`. Catalog-level fields: `schema_version` (`"2.0"`), `curated_at`, `catalog_sha256`, `count`.

## Examples

Filter active evaluation tools with the Python standard library:

```python
import json, urllib.request

url = "https://raw.githubusercontent.com/Anonymousyz/awesome-ai-production-readiness/main/data/resources.json"
catalog = json.load(urllib.request.urlopen(url))
active_eval = [
    r["name"] for r in catalog["resources"]
    if r["section"] == "Evaluation and testing" and r["status"] == "active"
]
print(active_eval)
```

List archived entries with `jq`:

```bash
curl -s https://raw.githubusercontent.com/Anonymousyz/awesome-ai-production-readiness/main/data/resources.json \
  | jq -r '.resources[] | select(.archived) | .name'
```

Verify integrity: recompute the SHA-256 of the compact-serialized `resources` array and compare it with `catalog_sha256` (the exact serialization is in `scripts/export_resources.py`, and `tests/test_catalog.py` shows the recomputation).

## Semantics to respect downstream

- Inclusion is not endorsement, and `status: "active"` only reflects the last curation review, not a live health check.
- `curated_at` is the catalog review date; `last_verified` is per-item and stays `null` unless an explicit item-level verification pass was run.
- Link and GitHub-metadata evidence lives in `data/link-check-report.json`, produced by the strict scheduled check in CI.

The catalog data is CC0-1.0 (see [`LICENSE-SCOPE.md`](../LICENSE-SCOPE.md)), so downstream reuse needs no attribution, though a link back helps others find updates.
