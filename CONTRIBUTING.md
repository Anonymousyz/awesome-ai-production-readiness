# Contributing

Contributions are welcome when they improve the production-readiness value of the list.

## Before proposing a resource

Read [`docs/curation_policy.md`](docs/curation_policy.md). Confirm that the resource is public, materially useful, and not included already.

## Entry format

```markdown
- [Project name](https://example.com) — State the concrete production-readiness use in one sentence.
```

A pull request should state:

- category and intended user;
- the production problem it addresses;
- maintenance status or authoritative-source status;
- whether the contributor is affiliated with the project;
- why an existing entry does not already cover the same use.

## Local checks

```bash
python scripts/export_resources.py --curated-at YYYY-MM-DD
python -m unittest discover -s tests -v
python scripts/check_links.py --metadata-policy strict
```

Access blocks or rate limits require manual review; do not remove a resource solely because a host rejects automated requests.

## Contribution license

By submitting a contribution, you agree to the path-level license in [`LICENSE-SCOPE.md`](LICENSE-SCOPE.md): catalog entries, generated catalog evidence, prose, and repository metadata are CC0-1.0; Python files under `scripts/` or `tests/`, `data/resources.schema.json`, and the CI template are MIT under [`LICENSE-CODE`](LICENSE-CODE). The root CC0 dedication does not apply to MIT-scoped paths. You must have the right to contribute the material; links and factual metadata do not transfer third-party code, trademark, patent, or content rights.

## Do not add

- private or pirated documents;
- referral links;
- generic AI directories;
- vendor pages with no reusable technical or governance content;
- a contributor's project without disclosing affiliation;
- projects unrelated to deployment, evaluation, governance, security, operations, or production readiness.
