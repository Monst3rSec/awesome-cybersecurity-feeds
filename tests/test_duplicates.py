import unittest

from scripts.validate_sources import validate_data
from tests.test_schema import DATA, SCHEMA, source


class DuplicateTests(unittest.TestCase):
    def test_url_normalization_trims_trailing_slash_and_case(self):
        first = source(website="https://Example.org/", feed={"url": "https://Example.org/feed/", "format": "rss"})
        second = source(id="another", name="Another", website="https://example.org", feed={"url": "https://example.org/feed", "format": "rss"})
        _, warnings = validate_data({**DATA, "entities": [first, second]}, SCHEMA)
        self.assertEqual(sum("duplicate feed URL" in warning for warning in warnings), 1)
        self.assertEqual(sum("duplicate website URL" in warning for warning in warnings), 1)

    def test_case_sensitive_paths_are_not_collapsed(self):
        first = source(feed={"url": "https://example.org/Feed", "format": "rss"})
        second = source(id="another", name="Another", website="https://another.example", feed={"url": "https://example.org/feed", "format": "rss"})
        _, warnings = validate_data({**DATA, "entities": [first, second]}, SCHEMA)
        self.assertFalse(any("duplicate feed URL" in warning for warning in warnings))


if __name__ == "__main__":
    unittest.main()
