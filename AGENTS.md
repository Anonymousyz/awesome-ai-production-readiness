# Agent instructions

This repository is a curated, machine-readable catalog of AI production-readiness resources. The English `README.md` is the single editorial source; everything else is derived or verified from it.

## Setup and verification

```bash
python -m pip install jsonschema   # optional; enables the schema instance-validation test
python -m unittest discover -s tests -v
```

After editing catalog entries in `README.md`, regenerate the committed export and rerun the tests:

```bash
python scripts/export_resources.py --curated-at YYYY-MM-DD   # use the current review date
python -m unittest discover -s tests -v
```

CI re-exports the catalog on every push and fails if `data/resources.json` does not match the README byte for byte.

## Hard rules

- Only add entries under the eleven registered `##` sections; the exporter fails on unregistered sections by design.
- Every entry needs a concrete production-readiness use. This is not a popularity list; inclusion is not endorsement.
- Do not edit `data/resources.json` by hand; it is generated. Do not overwrite `data/link-check-report.json` casually — it is committed release evidence produced by the strict link check (CI weekly schedule or `workflow_dispatch`).
- Archived or maintenance-review upstreams must carry the `**Archived upstream**;` / `**Maintenance review**;` markers so the machine status stays correct; tests lock the known cases.
- Licensing is path-scoped (`LICENSE-SCOPE.md`): catalog and prose are CC0-1.0, scripts/tests/schema/workflows are MIT. Keep new files inside the matrix.
- Record notable changes under `## Unreleased` in `CHANGELOG.md`. Releases are owner ceremonies with checksums.
