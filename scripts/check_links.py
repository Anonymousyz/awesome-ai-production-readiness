#!/usr/bin/env python3
"""Check catalog URLs without treating rate limits or access blocks as dead links."""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SOFT_STATUS = {401, 403, 405, 406, 418, 429}


def probe(url: str, timeout: float) -> dict:
    headers = {"User-Agent": "awesome-ai-production-readiness-link-check/0.3"}
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


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", default="data/resources.json")
    parser.add_argument("--output", default="data/link-check-report.json")
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args(argv)
    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    urls = [row["url"] for row in catalog["resources"]]
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(probe, url, args.timeout): url for url in urls}
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda row: row["url"])
    hard = [row for row in results if row["result"] in {"http_error", "network_error"}]
    payload = {
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "total": len(results),
        "hard_failures": len(hard),
        "results": results,
    }
    output = Path(args.output); output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Checked {len(results)} URLs; hard failures: {len(hard)}")
    return 1 if hard else 0


if __name__ == "__main__":
    raise SystemExit(main())
