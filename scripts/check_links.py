#!/usr/bin/env python3
"""Check catalog URLs plus GitHub canonical/archive metadata."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener, urlopen

SOFT_STATUS = {401, 403, 405, 406, 418, 429}


def _origin(url: str) -> tuple[str, str, int | None]:
    parsed = urlparse(url)
    try:
        port = parsed.port
    except ValueError:
        port = None
    if port is None:
        port = 443 if parsed.scheme.lower() == "https" else 80 if parsed.scheme.lower() == "http" else None
    return parsed.scheme.lower(), (parsed.hostname or "").lower(), port


class SafeGitHubRedirectHandler(HTTPRedirectHandler):
    """Keep authenticated GitHub API redirects on the exact HTTPS origin."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        allowed_origin = ("https", "api.github.com", 443)
        if req.has_header("Authorization") and (
            _origin(req.full_url) != allowed_origin or _origin(newurl) != allowed_origin
        ):
            raise HTTPError(
                req.full_url,
                code,
                "refusing authenticated cross-origin redirect",
                headers,
                fp,
            )
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def normalize_url(url: str) -> str:
    return url.rstrip("/").lower()


def request_headers(*, github_api: bool = False) -> dict[str, str]:
    headers = {"User-Agent": "awesome-ai-production-readiness-link-check/0.4"}
    if github_api:
        token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
    return headers


def probe(url: str, timeout: float) -> dict:
    headers = request_headers()
    for method in ("HEAD", "GET"):
        try:
            req = Request(url, headers=headers, method=method)
            with urlopen(req, timeout=timeout) as response:
                return {"url": url, "status": response.status, "result": "ok", "final_url": response.url}
        except HTTPError as exc:
            if exc.code in SOFT_STATUS:
                return {"url": url, "status": exc.code, "result": "blocked_or_rate_limited"}
            if method == "HEAD":
                continue
            return {"url": url, "status": exc.code, "result": "http_error"}
        except (URLError, TimeoutError, OSError) as exc:
            if method == "HEAD":
                continue
            return {"url": url, "status": None, "result": "network_error", "error": str(exc)}
    return {"url": url, "status": None, "result": "network_error"}


def github_coordinates(url: str) -> tuple[str, str] | None:
    parsed = urlparse(url)
    if parsed.hostname not in {"github.com", "www.github.com"}:
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    return parts[0], parts[1].removesuffix(".git")


def github_metadata(url: str, timeout: float) -> dict | None:
    coordinates = github_coordinates(url)
    if not coordinates:
        return None
    owner, repo = coordinates
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    try:
        req = Request(
            api_url,
            headers={**request_headers(github_api=True), "Accept": "application/vnd.github+json"},
        )
        opener = build_opener(SafeGitHubRedirectHandler())
        with opener.open(req, timeout=timeout) as response:
            data = json.load(response)
        return {
            "result": "ok",
            "full_name": data["full_name"],
            "archived": bool(data["archived"]),
            "canonical_url": data["html_url"],
            "pushed_at": data.get("pushed_at"),
        }
    except HTTPError as exc:
        return {
            "result": "blocked_or_rate_limited" if exc.code in SOFT_STATUS else "http_error",
            "status": exc.code,
        }
    except (URLError, TimeoutError, OSError, ValueError) as exc:
        return {"result": "network_error", "error": str(exc)}


def catalog_metadata_issues(row: dict, metadata: dict | None) -> list[str]:
    if not github_coordinates(row["canonical_url"]):
        return []
    if not metadata or metadata.get("result") != "ok":
        return ["metadata_unverified"]
    issues = []
    if normalize_url(row["canonical_url"]) != normalize_url(metadata["canonical_url"]):
        issues.append("canonical_url_mismatch")
    if bool(row["archived"]) != bool(metadata["archived"]):
        issues.append("archived_status_mismatch")
    if row["status"] == "archived" and not row["archived"]:
        issues.append("catalog_archived_flag_inconsistent")
    return issues


def check_row(row: dict, timeout: float) -> dict:
    result = probe(row["url"], timeout)
    metadata = github_metadata(row["canonical_url"], timeout)
    issues = catalog_metadata_issues(row, metadata)
    final_url = result.get("final_url")
    if (
        github_coordinates(row["canonical_url"])
        and final_url
        and normalize_url(final_url) != normalize_url(row["canonical_url"])
    ):
        issues.append("http_redirect_differs_from_canonical_url")
    result["catalog_status"] = row["status"]
    result["catalog_archived"] = row["archived"]
    if metadata:
        result["github"] = metadata
    result["catalog_issues"] = sorted(set(issues))
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default="data/resources.json")
    parser.add_argument("--output", default="data/link-check-report.json")
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument(
        "--metadata-policy",
        choices=("strict", "soft"),
        default="strict",
        help="strict fails when GitHub metadata is unverified; soft records coverage without failing",
    )
    args = parser.parse_args(argv)
    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    rows = catalog["resources"]
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check_row, row, args.timeout): row["url"] for row in rows}
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda row: row["url"])

    link_failures = [row for row in results if row["result"] in {"http_error", "network_error"}]
    github_rows = [row for row in results if "github" in row]
    metadata_verified = [row for row in github_rows if row["github"].get("result") == "ok"]
    metadata_unverified = [row for row in github_rows if row["github"].get("result") != "ok"]
    metadata_mismatches = [
        row
        for row in results
        if any(issue != "metadata_unverified" for issue in row["catalog_issues"])
    ]
    strict_unverified_failures = len(metadata_unverified) if args.metadata_policy == "strict" else 0
    hard_failures = len(link_failures) + len(metadata_mismatches) + strict_unverified_failures
    payload = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "catalog_sha256": catalog.get("catalog_sha256"),
        "metadata_policy": args.metadata_policy,
        "total": len(results),
        "hard_link_failures": len(link_failures),
        "github_metadata_total": len(github_rows),
        "github_metadata_verified": len(metadata_verified),
        "github_metadata_unverified": len(metadata_unverified),
        "catalog_metadata_failures": len(metadata_mismatches),
        "hard_failures": hard_failures,
        "results": results,
    }
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        f"Checked {len(results)} URLs; link failures: {len(link_failures)}; "
        f"metadata mismatches: {len(metadata_mismatches)}; "
        f"metadata unverified: {len(metadata_unverified)} ({args.metadata_policy})"
    )
    return 1 if hard_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
