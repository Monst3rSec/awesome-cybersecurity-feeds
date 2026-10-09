import unittest

from scripts.generate_readme import render_directory, update_readme
from tests.test_schema import DATA, source


class ReadmeTests(unittest.TestCase):
    def test_generation_is_deterministic_and_includes_categories(self):
        data = {**DATA, "entities": [source()]}
        first = render_directory(data)
        self.assertEqual(first, render_directory(data))
        self.assertIn("threat-news", first)
        self.assertIn("Sample", first)
        self.assertIn("| rss |", first)

    def test_readme_update_is_idempotent(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "README.md"
            path.write_text("# Test\n", encoding="utf-8")
            self.assertTrue(update_readme(path, DATA))
            first = path.read_text(encoding="utf-8")
            self.assertIn(render_directory(DATA), first)
            self.assertFalse(update_readme(path, DATA))
            self.assertEqual(first, path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
