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


if __name__ == "__main__":
    unittest.main()
