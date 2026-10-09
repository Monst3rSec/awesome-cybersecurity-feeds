import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.data_utils import load_dataset
from scripts.validate_sources import validate_data

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schema/security-feeds.schema.json").read_text(encoding="utf-8"))
DATA = load_dataset(ROOT / "security_feeds.yaml")
DATA = copy.deepcopy(DATA)
DATA["entities"] = []


def source(**overrides):
    record = {
        "id": "sample-source", "name": "Sample", "website": "https://example.org",
        "feed": {"url": "https://example.org/feed.xml", "format": "rss"},
        "categories": ["threat-news", "threat-research"], "sources": ["threat-feed-collection"],
        "status": "unverified",
    }
    record.update(overrides)
    return record


class SchemaTests(unittest.TestCase):
    def test_empty_canonical_dataset_is_valid(self):
        errors, warnings = validate_data(DATA, SCHEMA)
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_valid_record_supports_multiple_categories_and_optional_fields(self):
        data = copy.deepcopy(DATA)
        data["entities"] = [source(notes="Optional note")]
        self.assertEqual(validate_data(data, SCHEMA)[0], [])

    def test_missing_required_field_is_reported(self):
        item = source()
        del item["website"]
        errors, _ = validate_data({**DATA, "entities": [item]}, SCHEMA)
        self.assertTrue(any("website" in error for error in errors))

    def test_invalid_category_url_scheme_date_and_format_are_reported(self):
        item = source(website="ftp://example.org", categories=["not-registered"], last_verified="2025-02-30")
        item["feed"] = {"url": "https://example.org/feed", "format": "json"}
        errors, _ = validate_data({**DATA, "entities": [item]}, SCHEMA)
        self.assertGreaterEqual(len(errors), 4)

    def test_verified_record_requires_verification_date(self):
        errors, _ = validate_data({**DATA, "entities": [source(status="verified")]}, SCHEMA)
        self.assertTrue(any("last_verified" in error for error in errors))

    def test_duplicate_ids_are_blocking(self):
        errors, _ = validate_data({**DATA, "entities": [source(), source(id="sample-source", website="https://other.example", feed={"url": "https://other.example/feed", "format": "rss"})]}, SCHEMA)
        self.assertTrue(any("duplicate stable ID" in error for error in errors))

    def test_duplicate_urls_are_warnings(self):
        second = source(id="second-source", name="Second")
        _, warnings = validate_data({**DATA, "entities": [source(), second]}, SCHEMA)
        self.assertTrue(any("duplicate feed URL" in warning for warning in warnings))
        self.assertTrue(any("duplicate website URL" in warning for warning in warnings))

    def test_unknown_fields_are_rejected(self):
        item = source(unexpected="value")
        errors, _ = validate_data({**DATA, "entities": [item]}, SCHEMA)
        self.assertTrue(any("unexpected" in error for error in errors))

    def test_malformed_registries_return_validation_errors_without_crashing(self):
        data = copy.deepcopy(DATA)
        data["meta"]["categories"] = None
        data["meta"]["provenance"] = None
        errors, _ = validate_data(data, SCHEMA)
        self.assertTrue(any("meta.categories" in error for error in errors))
        self.assertTrue(any("meta.provenance" in error for error in errors))

    def test_yaml_parse_error_is_not_silently_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.yml"
            path.write_text("meta: [unterminated\n", encoding="utf-8")
            with self.assertRaises(Exception):
                load_dataset(path)

    def test_duplicate_yaml_mapping_key_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.yml"
            path.write_text("meta: {}\nmeta: {}\n", encoding="utf-8")
            with self.assertRaises(Exception):
                load_dataset(path)

    def test_embedded_url_credentials_are_rejected(self):
        item = source(website="https://user:secret@example.org")
        errors, _ = validate_data({**DATA, "entities": [item]}, SCHEMA)
        self.assertTrue(any("embedded credentials" in error for error in errors))

    def test_api_key_query_parameter_is_rejected_without_echoing_value(self):
        item = source(feed={"url": "https://example.org/feed?api_key=do-not-print", "format": "rss"})
        errors, _ = validate_data({**DATA, "entities": [item]}, SCHEMA)
        self.assertTrue(any("sensitive query parameter" in error for error in errors))
        self.assertFalse(any("do-not-print" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
