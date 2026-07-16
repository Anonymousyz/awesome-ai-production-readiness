# Maintenance record

- **Catalog schema:** 2.0 ([`data/resources.schema.json`](data/resources.schema.json))
- **Last manual curation review:** 2026-07-16
- **Review scope:** category relevance, duplicate URLs, canonical repository ownership, archive/maintenance status, concrete descriptions, public accessibility, and self-promotion risk
- **Machine-readable catalog:** [`data/resources.json`](data/resources.json)
- **Catalog-level date:** `curated_at` records when the catalog was reviewed/generated; it must be a valid, non-future ISO date and does not prove every linked resource was checked that day
- **Per-resource verification:** `last_verified` is nullable and is set only through the explicit `--verified-at` export option after every exported item has actually been checked; it must be valid, non-future, and not later than `curated_at`
- **Link-check report:** [`data/link-check-report.json`](data/link-check-report.json); the default `strict` metadata policy fails when GitHub canonical/archive metadata is unverified, while `soft` records incomplete coverage for diagnosis without treating it as a release pass

## Status meanings

- `ok`: the URL returned a successful response during the automated check.
- `blocked_or_rate_limited`: the host returned an access-control or rate-limit response; manual review may still show a live resource.
- `http_error`: a persistent non-access-control HTTP failure after HEAD/GET attempts.
- `network_error`: DNS, timeout, TLS, or other network failure; recheck before removal.
- `catalog_metadata_failures`: the catalog's canonical URL or archive flag disagrees with verified current GitHub metadata; fix before release.
- `github_metadata_unverified`: GitHub metadata could not be checked because of rate limiting, access control, or network failure; this fails under the default `strict` policy and is only non-blocking under explicitly selected `soft` diagnosis mode.

An automated response is not proof that the content is still relevant. Manual curation remains authoritative.
