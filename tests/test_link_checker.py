from pathlib import Path
import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError
from urllib.request import Request

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_links import SafeGitHubRedirectHandler, catalog_metadata_issues, github_coordinates, main, normalize_url, probe, request_headers


class LinkCheckerTests(unittest.TestCase):
    @patch.dict(os.environ, {"GITHUB_TOKEN": "test-token", "GH_TOKEN": ""}, clear=True)
    def test_github_token_is_only_added_for_github_api_requests(self):
        self.assertNotIn("Authorization", request_headers())
        self.assertEqual(
            request_headers(github_api=True).get("Authorization"),
            "Bearer test-token",
        )

    @patch.dict(os.environ, {"GITHUB_TOKEN": "test-token", "GH_TOKEN": ""}, clear=True)
    @patch("check_links.urlopen")
    def test_external_probe_request_never_receives_github_token(self, mock_urlopen):
        response = MagicMock()
        response.status = 200
        response.url = "https://example.org/resource"
        mock_urlopen.return_value.__enter__.return_value = response

        result = probe("https://example.org/resource", 1)

        request = mock_urlopen.call_args.args[0]
        self.assertEqual(result["result"], "ok")
        self.assertIsNone(request.get_header("Authorization"))

    def test_authenticated_github_request_refuses_cross_origin_redirects(self):
        handler = SafeGitHubRedirectHandler()
        request = Request(
            "https://api.github.com/repos/example/project",
            headers={"Authorization": "Bearer sentinel"},
        )
        for target in (
            "https://example.org/capture",
            "https://api.github.com:444/capture",
            "http://api.github.com/capture",
        ):
            with self.subTest(target=target), self.assertRaises(HTTPError):
                handler.redirect_request(request, None, 302, "Found", {}, target)

    def test_authenticated_github_request_allows_same_https_origin_redirect(self):
        handler = SafeGitHubRedirectHandler()
        request = Request(
            "https://api.github.com/repos/example/project",
            headers={"Authorization": "Bearer sentinel"},
        )
        redirected = handler.redirect_request(
            request, None, 302, "Found", {}, "https://api.github.com/repositories/1"
        )
        self.assertEqual(redirected.full_url, "https://api.github.com/repositories/1")

    def test_github_coordinates_accept_repo_urls(self):
        self.assertEqual(github_coordinates("https://github.com/microsoft/PyRIT"), ("microsoft", "PyRIT"))
        self.assertEqual(github_coordinates("https://github.com/microsoft/PyRIT.git"), ("microsoft", "PyRIT"))
        self.assertIsNone(github_coordinates("https://www.nist.gov/itl/ai-risk-management-framework"))

    def test_canonical_mismatch_is_a_catalog_failure(self):
        row = {
            "canonical_url": "https://github.com/Azure/PyRIT",
            "status": "active",
            "archived": False,
        }
        metadata = {
            "result": "ok",
            "canonical_url": "https://github.com/microsoft/PyRIT",
            "archived": False,
        }
        self.assertIn("canonical_url_mismatch", catalog_metadata_issues(row, metadata))

    def test_archive_mismatch_is_a_catalog_failure(self):
        row = {
            "canonical_url": "https://github.com/protectai/llm-guard",
            "status": "active",
            "archived": False,
        }
        metadata = {
            "result": "ok",
            "canonical_url": "https://github.com/protectai/llm-guard",
            "archived": True,
        }
        self.assertIn("archived_status_mismatch", catalog_metadata_issues(row, metadata))

    def test_matching_archived_catalog_row_passes(self):
        row = {
            "canonical_url": "https://github.com/protectai/llm-guard",
            "status": "archived",
            "archived": True,
        }
        metadata = {
            "result": "ok",
            "canonical_url": "https://github.com/protectai/llm-guard/",
            "archived": True,
        }
        self.assertEqual(catalog_metadata_issues(row, metadata), [])
        self.assertEqual(
            normalize_url(row["canonical_url"]),
            normalize_url(metadata["canonical_url"]),
        )

    def test_unverified_github_metadata_is_visible(self):
        row = {
            "canonical_url": "https://github.com/example/project",
            "status": "active",
            "archived": False,
        }
        self.assertEqual(
            catalog_metadata_issues(row, {"result": "blocked_or_rate_limited", "status": 403}),
            ["metadata_unverified"],
        )
        non_github = {**row, "canonical_url": "https://example.org/project"}
        self.assertEqual(catalog_metadata_issues(non_github, None), [])

    @patch("check_links.check_row")
    def test_strict_metadata_policy_fails_closed_and_soft_mode_reports(self, mock_check_row):
        mock_check_row.return_value = {
            "url": "https://github.com/example/project",
            "status": 200,
            "result": "ok",
            "catalog_status": "active",
            "catalog_archived": False,
            "github": {"result": "blocked_or_rate_limited", "status": 403},
            "catalog_issues": ["metadata_unverified"],
        }
        catalog = {
            "catalog_sha256": "0" * 64,
            "resources": [{
                "url": "https://github.com/example/project",
                "canonical_url": "https://github.com/example/project",
                "status": "active",
                "archived": False,
            }],
        }
        with tempfile.TemporaryDirectory() as tmp:
            catalog_path = Path(tmp) / "catalog.json"
            strict_path = Path(tmp) / "strict.json"
            soft_path = Path(tmp) / "soft.json"
            catalog_path.write_text(json.dumps(catalog), encoding="utf-8")
            self.assertEqual(main(["--catalog", str(catalog_path), "--output", str(strict_path)]), 1)
            self.assertEqual(
                main(["--catalog", str(catalog_path), "--output", str(soft_path), "--metadata-policy", "soft"]),
                0,
            )
            strict = json.loads(strict_path.read_text(encoding="utf-8"))
            soft = json.loads(soft_path.read_text(encoding="utf-8"))
            for payload in (strict, soft):
                self.assertEqual(payload["github_metadata_total"], 1)
                self.assertEqual(payload["github_metadata_verified"], 0)
                self.assertEqual(payload["github_metadata_unverified"], 1)
            self.assertEqual(strict["hard_failures"], 1)
            self.assertEqual(soft["hard_failures"], 0)


if __name__ == "__main__":
    unittest.main()
