import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from export_resources import extract, main


class CatalogTests(unittest.TestCase):
    def test_catalog_has_at_least_fifty_unique_resources(self):
        rows = extract(ROOT / "README.md")
        self.assertGreaterEqual(len(rows), 50)
        self.assertEqual(len(rows), len({row["url"] for row in rows}))

    def test_each_resource_has_required_fields(self):
        for row in extract(ROOT / "README.md"):
            self.assertTrue(row["name"].strip())
            self.assertTrue(row["description"].strip())
            self.assertTrue(row["url"].startswith(("https://", "http://")))
            self.assertNotEqual(row["category"], "Uncategorized")

    def test_export_is_valid_and_counted(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "resources.json"
            self.assertEqual(main(["--readme", str(ROOT / "README.md"), "--output", str(out), "--curated-at", "2026-07-15"]), 0)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["count"], len(data["resources"]))
            self.assertEqual(data["curated_at"], "2026-07-15")

    def test_duplicate_urls_in_markdown_are_rejected_not_silently_dropped(self):
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "README.md"
            readme.write_text(
                "## Evaluation\n"
                "- [One](https://example.org/tool): first\n"
                "- [Two](https://example.org/tool): duplicate\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "duplicate resource URL"):
                extract(readme)

    def test_recommended_set_does_not_start_with_archived_projects(self):
        text = (ROOT / "docs" / "recommended_starting_set.md").read_text(encoding="utf-8")
        self.assertNotIn("tensorflow/model-card-toolkit", text)

    def test_archived_resources_are_explicitly_labeled(self):
        rows = {row["url"]: row for row in extract(ROOT / "README.md")}
        for url in (
            "https://github.com/protectai/rebuff",
            "https://github.com/tensorflow/model-card-toolkit",
        ):
            self.assertIn("archived", rows[url]["description"].lower())


if __name__ == "__main__":
    unittest.main()
