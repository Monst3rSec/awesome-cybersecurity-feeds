import io
import unittest
import urllib.error
from unittest.mock import patch
from email.message import Message

from scripts.check_feeds import check_one, detect_feed
from tests.test_schema import source


RSS = b'<?xml version="1.0"?><rss version="2.0"><channel><title>Example</title></channel></rss>'
ATOM = b'<feed xmlns="http://www.w3.org/2005/Atom"><title>Example</title></feed>'
BAD_XML = b'<rss><channel>'


class FakeResponse:
    status = 200
    headers = Message()
    def __init__(self, body):
        self.body = body
    def __enter__(self):
        return self
    def __exit__(self, *args):
        return None
    def read(self, size=-1):
        return self.body[:size]
    def getcode(self):
        return self.status


class FakeOpener:
    def __init__(self, response=None, error=None):
        self.response, self.error = response, error
    def open(self, request, timeout=None):
        if self.error:
            raise self.error
        return self.response


class SequenceOpener:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
    def open(self, request, timeout=None):
        outcome = next(self.outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class FeedCheckTests(unittest.TestCase):
    def test_detects_supported_xml_roots(self):
        self.assertEqual(detect_feed(RSS), "rss")
        self.assertEqual(detect_feed(ATOM), "atom")
        self.assertEqual(detect_feed(b'<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"/>'), "rdf")
        self.assertIsNone(detect_feed(BAD_XML))

    def test_healthy_and_format_mismatch(self):
        self.assertEqual(check_one(source(), FakeOpener(FakeResponse(RSS)), retries=0)["health"], "healthy")
        item = source()
        item["feed"]["format"] = "atom"
        result = check_one(item, FakeOpener(FakeResponse(RSS)), retries=0)
        self.assertEqual(result["health"], "degraded")
        self.assertEqual(result["detected_format"], "rss")

    def test_malformed_document_is_broken(self):
        self.assertEqual(check_one(source(), FakeOpener(FakeResponse(BAD_XML)), retries=0)["health"], "broken")

    def test_forbidden_and_rate_limited_responses_are_inconclusive(self):
        for status in (403, 429):
            error = urllib.error.HTTPError("https://example.org/feed.xml", status, "limited", Message(), io.BytesIO())
            result = check_one(source(), FakeOpener(error=error), retries=0)
            self.assertEqual(result["health"], "inconclusive")
            self.assertEqual(result["http_status"], status)

    def test_not_found_is_confirmed_broken(self):
        error = urllib.error.HTTPError("https://example.org/feed.xml", 404, "missing", Message(), io.BytesIO())
        self.assertEqual(check_one(source(), FakeOpener(error=error), retries=0)["health"], "broken")

    def test_transient_server_error_retries_then_recovers(self):
        error = urllib.error.HTTPError("https://example.org/feed.xml", 503, "unavailable", Message(), io.BytesIO())
        with patch("scripts.check_feeds.time.sleep") as sleep:
            result = check_one(source(), SequenceOpener([error, FakeResponse(RSS)]), retries=1)
        self.assertEqual(result["health"], "healthy")
        sleep.assert_called_once()

    def test_timeout_is_inconclusive_without_crashing(self):
        result = check_one(source(), FakeOpener(error=TimeoutError("timed out")), retries=0)
        self.assertEqual(result["health"], "inconclusive")
        self.assertIn("timed out", result["error"])

    def test_html_is_rejected_as_non_feed(self):
        result = check_one(source(), FakeOpener(FakeResponse(b"<!doctype html><html></html>")), retries=0)
        self.assertEqual(result["health"], "broken")


if __name__ == "__main__":
    unittest.main()
