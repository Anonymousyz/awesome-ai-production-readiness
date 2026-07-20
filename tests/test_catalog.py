import hashlib
import json
from datetime import date, timedelta
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from export_resources import build_catalog, main, parse_resources

TEST_DATE = "2026-07-16"


class CatalogTests(unittest.TestCase):
    def rows(self):
        return parse_resources(ROOT / "README.md")

    def test_catalog_has_fifty_seven_unique_resources(self):
        rows = self.rows()
        self.assertEqual(len(rows), 57)
        self.assertEqual(len(rows), len({row["url"].rstrip("/").lower() for row in rows}))

    def test_each_resource_has_stable_machine_fields(self):
        required = {
            "name",
            "url",
            "canonical_url",
            "description",
            "section",
            "type",
            "status",
            "archived",
            "license",
            "last_verified",
            "authoritative_source",
        }
        for row in self.rows():
            self.assertEqual(set(row), required)
            self.assertTrue(row["name"].strip())
            self.assertTrue(row["description"].strip())
            self.assertNotIn("**", row["description"])
            self.assertEqual(row["url"], row["canonical_url"])
            self.assertIsNone(row["last_verified"])
            self.assertIn(row["status"], {"active", "maintenance-review", "archived"})
            self.assertEqual(row["archived"], row["status"] == "archived")

    def test_committed_artifact_matches_readme_export(self):
        committed = json.loads((ROOT / "data" / "resources.json").read_text(encoding="utf-8"))
        generated = build_catalog(ROOT / "README.md", committed["curated_at"])
        self.assertEqual(committed, generated)
        self.assertEqual(committed["schema_version"], "2.0")
        self.assertEqual(committed["count"], 57)
        serialized = json.dumps(committed["resources"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        self.assertEqual(committed["catalog_sha256"], hashlib.sha256(serialized.encode("utf-8")).hexdigest())

    def test_public_json_schema_declares_all_machine_fields(self):
        schema = json.loads((ROOT / "data" / "resources.schema.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schema_version"]["const"], "2.0")
        self.assertEqual(
            schema["$id"],
            "https://raw.githubusercontent.com/Anonymousyz/awesome-ai-production-readiness/v0.3.4/data/resources.schema.json",
        )
        self.assertIn("count", schema.get("$comment", ""))
        resource = schema["$defs"]["resource"]
        self.assertIn("canonical_url", resource["required"])
        self.assertIn("status", resource["required"])
        self.assertIn("last_verified", resource["required"])
        self.assertEqual(resource["properties"]["last_verified"]["type"], ["string", "null"])
        self.assertEqual(len(resource["allOf"]), 2)

    def test_export_requires_explicit_review_date(self):
        with tempfile.TemporaryDirectory() as tmp, patch("sys.stderr"):
            with self.assertRaises(SystemExit):
                main(["--readme", str(ROOT / "README.md"), "--output", str(Path(tmp) / "out.json")])

    def test_export_is_valid_and_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "resources.json"
            self.assertEqual(
                main([
                    "--readme",
                    str(ROOT / "README.md"),
                    "--output",
                    str(out),
                    "--curated-at",
                    TEST_DATE,
                ]),
                0,
            )
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["count"], len(data["resources"]))
            self.assertEqual(data["curated_at"], TEST_DATE)
            self.assertTrue(all(row["last_verified"] is None for row in data["resources"]))

    def test_full_verification_date_requires_explicit_opt_in(self):
        rows = parse_resources(ROOT / "README.md", TEST_DATE)
        self.assertTrue(rows)
        self.assertTrue(all(row["last_verified"] == TEST_DATE for row in rows))

    def test_export_rejects_invalid_future_and_out_of_order_dates(self):
        tomorrow = (date.today() + timedelta(days=1)).isoformat()
        for curated_at, verified_at in (
            ("not-a-date", None),
            ("2026-02-30", None),
            (tomorrow, None),
            (TEST_DATE, "not-a-date"),
            (TEST_DATE, tomorrow),
            ("20260716", None),
            ("2026-W29-4", None),
        ):
            with self.subTest(curated_at=curated_at, verified_at=verified_at):
                with self.assertRaises(ValueError):
                    build_catalog(ROOT / "README.md", curated_at, verified_at)

    def test_duplicate_urls_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(
                "## Evaluation and testing\n"
                "- [One](https://example.org/tool): first\n"
                "- [Two](https://example.org/tool): duplicate\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate resource URL"):
                parse_resources(readme, TEST_DATE)

    def test_contribution_em_dash_format_is_exported(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(
                "## Evaluation and testing\n"
                "- [One](https://example.org/tool) — contribution format\n",
                encoding="utf-8",
            )
            rows = parse_resources(readme, TEST_DATE)
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["name"], "One")

    def test_resource_bullets_under_unregistered_sections_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(
                "## Brand-new section\n"
                "- [One](https://example.org/tool): must not be silently dropped\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "unregistered section"):
                parse_resources(readme, TEST_DATE)

    def test_committed_catalog_validates_against_public_json_schema(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema is not installed")
        catalog = json.loads((ROOT / "data" / "resources.json").read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "data" / "resources.schema.json").read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)
        validator = jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker())
        validator.validate(catalog)

    def test_archived_and_maintenance_resources_are_machine_labeled(self):
        rows = {row["url"]: row for row in self.rows()}
        for url in (
            "https://github.com/protectai/rebuff",
            "https://github.com/protectai/llm-guard",
            "https://github.com/tensorflow/model-card-toolkit",
        ):
            self.assertEqual(rows[url]["status"], "archived")
            self.assertTrue(rows[url]["archived"])
        for url in (
            "https://github.com/whylabs/whylogs",
            "https://github.com/Azure/counterfit",
        ):
            self.assertEqual(rows[url]["status"], "maintenance-review")

    def test_known_moved_repositories_use_canonical_urls(self):
        urls = {row["url"] for row in self.rows()}
        current = {
            "https://github.com/microsoft/PyRIT",
            "https://github.com/Giskard-AI/giskard-oss",
            "https://github.com/vibrantlabsai/ragas",
            "https://github.com/treeverse/dvc",
            "https://github.com/data-privacy-stack/presidio",
            "https://github.com/anthropics/claude-cookbooks",
        }
        stale = {
            "https://github.com/Azure/PyRIT",
            "https://github.com/Giskard-AI/giskard",
            "https://github.com/explodinggradients/ragas",
            "https://github.com/iterative/dvc",
            "https://github.com/microsoft/presidio",
            "https://github.com/anthropics/anthropic-cookbook",
        }
        self.assertTrue(current <= urls)
        self.assertFalse(stale & urls)

    def test_recommended_set_excludes_archived_projects(self):
        text = (ROOT / "docs" / "recommended_starting_set.md").read_text(encoding="utf-8").lower()
        for archived in ("tensorflow/model-card-toolkit", "protectai/llm-guard", "azure/pyrit"):
            self.assertNotIn(archived, text)

    def test_production_path_connects_the_three_public_repositories(self):
        text = (ROOT / "docs" / "production_path.md").read_text(encoding="utf-8")
        self.assertIn("ai-prototype-to-production-toolkit", text)
        self.assertIn("research-to-decision-toolkit", text)
        self.assertIn("accountable human judgment", text)

    def test_license_matrix_and_chinese_v2_boundaries_are_explicit(self):
        scope = (ROOT / "LICENSE-SCOPE.md").read_text(encoding="utf-8-sig")
        readme = (ROOT / "README.md").read_text(encoding="utf-8-sig")
        zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8-sig")
        code_license = (ROOT / "LICENSE-CODE").read_text(encoding="utf-8-sig")
        for path in (
            "data/resources.schema.json",
            "docs/github_actions_catalog.template.yml",
            ".github/workflows/catalog.yml",
            "data/link-check-report.json",
            "scripts/",
            "tests/",
        ):
            self.assertIn(path, scope)
        self.assertIn("LICENSE-SCOPE.md", readme)
        self.assertIn("does not apply", code_license)
        for phrase in ("json schema", "canonical", "curated_at", "last_verified", "strict"):
            self.assertIn(phrase, zh.lower())
        workflow = (ROOT / "docs" / "github_actions_catalog.template.yml").read_text(encoding="utf-8-sig")
        self.assertIn("permissions:\n  contents: read", workflow)
        self.assertIn("GITHUB_TOKEN: ${{ github.token }}", workflow)
        self.assertIn("if: always()", workflow)

    def test_committed_link_report_exposes_metadata_coverage(self):
        report = json.loads((ROOT / "data" / "link-check-report.json").read_text(encoding="utf-8"))
        self.assertEqual(
            report["github_metadata_total"],
            report["github_metadata_verified"] + report["github_metadata_unverified"],
        )
        self.assertEqual(report["metadata_policy"], "strict")
        self.assertEqual(
            report["hard_failures"],
            report["hard_link_failures"]
            + report["catalog_metadata_failures"]
            + report["github_metadata_unverified"],
        )

    def test_ci_template_reuses_committed_date_and_always_uploads_report(self):
        text = (ROOT / "docs" / "github_actions_catalog.template.yml").read_text(encoding="utf-8")
        self.assertIn("data/resources.json", text)
        self.assertIn("--curated-at", text)
        self.assertIn("if: always()", text)


if __name__ == "__main__":
    unittest.main()
