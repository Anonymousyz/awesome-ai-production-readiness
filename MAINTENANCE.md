# Maintenance record

- **Catalog schema:** 1
- **Last manual curation review:** 2026-07-15
- **Review scope:** category relevance, duplicate URLs, concrete descriptions, public accessibility, and self-promotion risk
- **Machine-readable catalog:** [`data/resources.json`](data/resources.json)
- **Link-check report:** [`data/link-check-report.json`](data/link-check-report.json) when generated

## Status meanings

- `ok`: the URL returned a successful response during the automated check.
- `blocked_or_rate_limited`: the host returned an access-control or rate-limit response; manual review may still show a live resource.
- `http_error`: a persistent non-access-control HTTP failure after HEAD/GET attempts.
- `network_error`: DNS, timeout, TLS, or other network failure; recheck before removal.

An automated response is not proof that the content is still relevant. Manual curation remains authoritative.
