#!/usr/bin/env python3
"""Check feeds conservatively and emit a JSON health report (never edits the dataset)."""
from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from scripts.data_utils import load_dataset

USER_AGENT = "awesome-cybersecurity-feeds-health-check/1.0 (+https://github.com/Monst3rSec/awesome-cybersecurity-feeds)"
MAX_BYTES = 1_000_000


class SafeRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Permit HTTP(S) redirects but reject scheme changes and HTTPS downgrade."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old_scheme = urllib.parse.urlparse(req.full_url).scheme.lower()
        new_scheme = urllib.parse.urlparse(newurl).scheme.lower()
        if new_scheme not in {"http", "https"} or (old_scheme == "https" and new_scheme != "https"):
            raise urllib.error.URLError("unsafe redirect rejected")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def detect_feed(payload: bytes) -> str | None:
    try:
        root = ET.fromstring(payload)
    except (ET.ParseError, ValueError):
        return None
    tag = root.tag
    local = tag.rsplit("}", 1)[-1].split(":")[-1].lower() if isinstance(tag, str) else ""
    if local == "rss":
        return "rss"
    if local == "feed" and ("atom" in tag.lower() or tag == "feed"):
        return "atom"
    if local == "rdf" and ("rdf" in tag.lower() or tag == "rdf"):
        return "rdf"
    return None


def check_one(entity: dict, opener=None, timeout: float = 10, retries: int = 2) -> dict:
    """Check one record; network outcomes distinguish confirmed from inconclusive."""
    opener = opener or urllib.request.build_opener(SafeRedirectHandler())
    url = entity["feed"]["url"]
    expected = entity["feed"]["format"]
    result = {
        "id": entity["id"], "name": entity["name"], "feed_url": url,
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "http_status": None, "detected_format": None, "health": "inconclusive",
        "error": None, "recommended_action": "Recheck manually from a permitted network.",
    }
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        result.update(health="broken", error="Feed URL is not a valid HTTP(S) URL.", recommended_action="Correct the feed URL in a reviewed pull request.")
        return result
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/atom+xml, application/rss+xml, application/xml, text/xml;q=0.9, */*;q=0.1"})
    for attempt in range(retries + 1):
        try:
            with opener.open(request, timeout=timeout) as response:
                status = getattr(response, "status", response.getcode())
                result["http_status"] = status
                if status >= 500:
                    raise urllib.error.HTTPError(url, status, "server error", response.headers, None)
                if status in (403, 429):
                    result.update(health="inconclusive", error=f"HTTP {status}; access may be restricted or rate limited.", recommended_action="Do not bypass controls; retry later or confirm the published feed URL manually.")
                    return result
                if status >= 400:
                    result.update(health="broken", error=f"HTTP {status}", recommended_action="Confirm the official feed URL; propose a correction or removal after manual review.")
                    return result
                payload = response.read(MAX_BYTES + 1)
                if len(payload) > MAX_BYTES:
                    result.update(health="degraded", error=f"Response exceeds {MAX_BYTES} byte safety limit.", recommended_action="Review the feed endpoint manually; automated checks do not download larger documents.")
                    return result
            detected = detect_feed(payload)
            result["detected_format"] = detected
            if detected is None:
                result.update(health="broken", error="Response is not a well-formed RSS, Atom, or RDF feed.", recommended_action="Check whether the URL serves a feed document and whether it is temporarily malformed.")
            elif detected != expected:
                result.update(health="degraded", error=f"Declared format is {expected}, detected {detected}.", recommended_action="Review the declared format and update the record if needed.")
            else:
                result.update(health="healthy", error=None, recommended_action="No action needed.")
            return result
        except urllib.error.HTTPError as exc:
            result["http_status"] = exc.code
            if exc.code in (403, 429):
                result.update(health="inconclusive", error=f"HTTP {exc.code}; access may be restricted or rate limited.", recommended_action="Do not bypass controls; retry later or confirm the published feed URL manually.")
                return result
            if exc.code in (404, 410):
                result.update(health="broken", error=f"HTTP {exc.code}", recommended_action="Confirm the official feed URL; propose a correction or removal after manual review.")
                return result
            if exc.code < 500:
                result.update(health="broken", error=f"HTTP {exc.code}", recommended_action="Review the endpoint manually; the server rejected the request.")
                return result
            result["error"] = f"HTTP {exc.code} server error"
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            result["error"] = str(getattr(exc, "reason", exc))[:300]
        except Exception as exc:  # malformed response implementations should not stop a batch
            result["error"] = f"Unexpected check error: {type(exc).__name__}: {str(exc)[:200]}"
        if attempt < retries:
            time.sleep(min(2 ** attempt, 4))
    result["health"] = "degraded" if result["http_status"] and result["http_status"] >= 500 else "inconclusive"
    result["recommended_action"] = "Retry later and verify from another permitted network; automated failure alone does not justify changing the curated record."
    return result


def run_checks(entities: list[dict], delay: float = 1.0, timeout: float = 10, retries: int = 2) -> dict:
    # Sequential checks ensure two records on the same domain are never checked concurrently.
    opener = urllib.request.build_opener(SafeRedirectHandler())
    report = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "results": []}
    last_check_by_domain = {}
    for entity in entities:
        domain = (urllib.parse.urlparse(entity["feed"]["url"]).hostname or "").lower()
        if domain in last_check_by_domain:
            wait = delay - (time.monotonic() - last_check_by_domain[domain])
            if wait > 0:
                time.sleep(wait)
        result = check_one(entity, opener=opener, timeout=timeout, retries=retries)
        report["results"].append(result)
        last_check_by_domain[domain] = time.monotonic()
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "security_feeds.yaml")
    parser.add_argument("--output", type=Path, default=Path("feed-health.json"))
    parser.add_argument("--delay", type=float, default=1.0, help="minimum seconds between checks on one domain")
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--retries", type=int, default=2)
    args = parser.parse_args()
    if args.delay < 0 or args.timeout <= 0 or args.retries < 0:
        parser.error("delay must be nonnegative; timeout must be positive; retries must be nonnegative")
    dataset = load_dataset(args.data)
    report = run_checks(dataset.get("entities", []), args.delay, args.timeout, args.retries)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(report['results'])} feed result(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
