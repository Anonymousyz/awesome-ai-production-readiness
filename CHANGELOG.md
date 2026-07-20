# Changelog

## Unreleased

- Published the catalog-validation workflow to `.github/workflows/catalog.yml` from the documented template, now that a workflow-scope credential is available: pushes and pull requests rebuild the catalog and run the tests; the strict live link check stays on the weekly schedule and manual dispatch.
- Refreshed `data/link-check-report.json` from the first authenticated strict run on CI infrastructure: 57/57 URLs respond, 46/46 GitHub metadata records verified, zero hard failures. This replaces the credential-free 2026-07-16 report that carried three unverified records, and the committed report is now tested as a clean release gate (`hard_failures == 0`, matching catalog SHA256).
- Made the exporter fail on resource bullets under unregistered sections instead of silently dropping them, and added a regression test for that failure mode.
- Added an optional test that validates the committed `data/resources.json` against the public JSON Schema when `jsonschema` is installed; CI installs it, and the test skips cleanly in bare local environments.
- Added a Cursor cloud-agent environment definition (`.cursor/environment.json`).
- Extended the license matrix to cover `assets/` (CC0) and the `.github/` workflow and issue-form files (MIT), which were added after the matrix was written.
- Added the active-workflow badge, a bilingual maintenance-pipeline diagram, and a Chinese gap-to-tool quick map.

## v0.3.4 — 2026-07-16

- Replaced six moved GitHub URLs with their canonical repositories and marked LLM Guard as archived upstream.
- Added machine-readable archive and maintenance-review states for LLM Guard, Rebuff, Model Card Toolkit, WhyLogs, and Counterfit.
- Upgraded the catalog to schema 2.0 with a versioned raw JSON Schema identifier, bidirectional archive-state invariants, canonical URLs, resource types, nullable per-item verification dates, and a deterministic catalog SHA256.
- Made the committed `data/resources.json` part of the test contract and accepted the documented em-dash contribution format.
- Added live GitHub canonical/archive checks; the default strict policy now fails closed and reports metadata coverage instead of silently accepting rate limits or network errors.
- Validated `curated_at` and `last_verified` as exact `YYYY-MM-DD`, real, non-future dates and enforced `last_verified <= curated_at`.
- Scoped `GITHUB_TOKEN` / `GH_TOKEN` to `api.github.com` metadata requests only, refused authenticated redirects outside the exact `https://api.github.com:443` origin, and ensured catalog URL probes never receive authentication headers.
- Repaired the public CI template to reuse the committed review date, explicitly inject the built-in read-only GitHub token into the strict metadata step, and upload link diagnostics even when strict verification fails.
- Added a path-level license matrix separating CC0 catalog/prose/evidence from MIT scripts, tests, schema, and CI template, with matching English and Chinese guidance.
- Updated the Hugging Face Model Cards entry to the stable explicit-English documentation URL; the credential-free strict report verifies 43 of 46 GitHub metadata records and exposes the remaining three as release-blocking rather than silently passing them.

## v0.3.3 — 2026-07-16

- Added citation metadata, security reporting guidance, and contributor conduct rules.
- Expanded the Chinese entry point from a short summary into a usable navigation page.
- Re-ran the 57-resource catalog export, duplicate probe, unit tests, and live-link scan without changing the catalog schema.

## v0.3.2 — 2026-07-16

- Expanded the repository introduction with target readers, operating questions, and catalog-governance mechanics.
- Added a professional entry point for product leads, platform engineers, risk reviewers, and FDE / solution architects.
- Preserved the v0.3.1 catalog format, curation rules, archived-resource boundary, and verification contract.

## v0.3.1 — 2026-07-15

- Made duplicate curated URLs a hard export failure instead of silently discarding later entries.
- Removed cross-category duplicates from the catalog.
- Labeled archived upstream projects explicitly and removed archived Model Card Toolkit from the recommended starting set.
- Added regression tests for duplicate source entries and archived recommendations.
- Added a production workflow path that connects tool discovery, readiness evidence, operating controls, and human decision packets.

## v0.3.0 — 2026-07-15

- Added a versioned machine-readable resource catalog.
- Added export, duplicate, schema, and link-check tooling.
- Published curation, exclusion, affiliation, and maintenance rules.
- Added a compact recommended starting set.
- Disclosed maintainer-authored entries and removed non-evidentiary badges.

## v0.2.2

- Added the production-readiness lens and manifesto link.
- Expanded the curated list to more than 50 unique resources.
- Added a quick decision map and Chinese introduction.
