# License scope by path

This repository uses file-level licensing. The root `LICENSE` and `LICENSE-CODE` do not apply to every file indiscriminately.

## CC0-1.0 catalog and prose

The CC0-1.0 dedication in [`LICENSE`](LICENSE) applies to original catalog data, generated catalog evidence, prose, and repository metadata, including:

- `README.md` and `README.zh-CN.md`;
- top-level governance and citation documents such as `CHANGELOG.md`, `CONTRIBUTING.md`, `MAINTENANCE.md`, and `CITATION.cff`;
- Markdown files under `docs/`;
- images and generated artwork under `assets/`;
- `data/resources.json`;
- `data/link-check-report.json`.

## MIT automation and machine contract

The MIT license in [`LICENSE-CODE`](LICENSE-CODE) applies only to:

- Python files under `scripts/`;
- Python files under `tests/`;
- `data/resources.schema.json`;
- `docs/github_actions_catalog.template.yml`;
- `.github/workflows/catalog.yml`;
- YAML issue-form definitions under `.github/ISSUE_TEMPLATE/`.

The root CC0 dedication does not apply to these MIT-scoped paths. These files are not dual-licensed unless an individual file explicitly says otherwise.

## Excluded third-party rights

Names, descriptions, links, trademarks, patents, and source code belonging to listed projects retain their own rights. Inclusion in this catalog does not relicense, certify, endorse, or verify those projects. GitHub-generated source archives also contain both license scopes; users must apply the matrix above to each path.
