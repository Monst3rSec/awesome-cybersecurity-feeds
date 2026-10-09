#!/usr/bin/env python3
"""Validate the canonical YAML dataset and generated README."""
from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import parse_qsl, urlsplit

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from jsonschema import Draft202012Validator, FormatChecker
from scripts.data_utils import load_dataset
from scripts.generate_readme import render_directory

SUPPORTED_CATEGORIES = {
    "ai-soc-vendor", "threat-news", "threat-research", "government-cert", "vulnerability-exploit"
}
SUPPORTED_PROVENANCE = {"ai-soc-vendor-directory", "threat-feed-collection"}


def normalized_url(value: str) -> str:
    """Normalize host and default port while preserving case-sensitive paths."""
    try:
        parts = urlsplit(value)
    except ValueError:
        return value
    try:
        port = parts.port
    except ValueError:
        return value
    host = (parts.hostname or "").lower()
    if port and not ((parts.scheme.lower() == "https" and port == 443) or (parts.scheme.lower() == "http" and port == 80)):
        host = f"{host}:{port}"
    path = parts.path.rstrip("/") or "/"
    return f"{parts.scheme.lower()}://{host}{path}" + (f"?{parts.query}" if parts.query else "")


def check_url(value: str, location: str, errors: list[str]) -> None:
    try:
        parts = urlsplit(value)
        if parts.scheme.lower() not in {"http", "https"} or not parts.hostname:
            raise ValueError("must be an absolute HTTP(S) URL with a hostname")
        _ = parts.port
        if parts.username is not None or parts.password is not None:
            raise ValueError("must not contain embedded credentials")
        if any(character.isspace() for character in value):
            raise ValueError("must not contain whitespace")
        sensitive = {"api_key", "apikey", "access_token", "auth", "authorization", "client_secret", "key", "password", "secret", "signature", "token"}
        query_keys = {key.casefold().replace("-", "_") for key, _ in parse_qsl(parts.query, keep_blank_values=True)}
        exposed = sorted(query_keys & sensitive)
        if exposed:
            raise ValueError(f"contains sensitive query parameter(s): {', '.join(exposed)}")
    except ValueError as exc:
        errors.append(f"{location}: invalid URL ({exc})")



def validate_data(data: dict, schema: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    for error in sorted(validator.iter_errors(data), key=lambda e: list(map(str, e.absolute_path))):
        location = ".".join(map(str, error.absolute_path)) or "dataset"
        errors.append(f"{location}: {error.message}")

    entities = data.get("entities", [])
    if not isinstance(entities, list):
        return errors, warnings
    ids: dict[str, int] = {}
    feeds: dict[str, list[str]] = defaultdict(list)
    websites: dict[str, list[str]] = defaultdict(list)
    for index, entity in enumerate(entities):
        if not isinstance(entity, dict):
            continue
        source_id = entity.get("id", f"entities[{index}]")
        if isinstance(source_id, str):
            if source_id in ids:
                errors.append(f"{source_id}.id: duplicate stable ID (also entities[{ids[source_id]}])")
            else:
                ids[source_id] = index
        feed = entity.get("feed")
        if isinstance(feed, dict) and isinstance(feed.get("url"), str):
            check_url(feed["url"], f"{source_id}.feed.url", errors)
            feeds[normalized_url(feed["url"])].append(str(source_id))
        if isinstance(entity.get("website"), str):
            check_url(entity["website"], f"{source_id}.website", errors)
            websites[normalized_url(entity["website"])].append(str(source_id))
        if entity.get("status") == "verified" and not entity.get("last_verified"):
            errors.append(f"{source_id}.last_verified: required when status is verified")
    for url, source_ids in feeds.items():
        if len(source_ids) > 1:
            warnings.append(f"duplicate feed URL shared by {', '.join(source_ids)}: {url}")
    for url, source_ids in websites.items():
        if len(source_ids) > 1:
            warnings.append(f"duplicate website URL shared by {', '.join(source_ids)}: {url}")
    meta = data.get("meta", {})
    if isinstance(meta, dict):
        raw_categories = meta.get("categories", [])
        if not isinstance(raw_categories, list):
            raw_categories = []
        category_ids = [c.get("id") for c in raw_categories if isinstance(c, dict) and isinstance(c.get("id"), str)]
        if len(category_ids) != len(set(category_ids)):
            errors.append("meta.categories: category IDs must be unique")
        if set(category_ids) != SUPPORTED_CATEGORIES:
            errors.append("meta.categories: registry must contain each supported category exactly once")
        raw_provenance = meta.get("provenance", [])
        if not isinstance(raw_provenance, list):
            raw_provenance = []
        provenance = [value for value in raw_provenance if isinstance(value, str)]
        if len(provenance) != len(set(provenance)):
            errors.append("meta.provenance: provenance identifiers must be unique")
        if set(provenance) != SUPPORTED_PROVENANCE:
            errors.append("meta.provenance: registry must contain each supported provenance identifier exactly once")
        allowed_categories = set(category_ids)
        allowed_provenance = set(provenance)
        for entity in entities:
            if not isinstance(entity, dict):
                continue
            source_id = entity.get("id", "<unknown>")
            if isinstance(entity.get("categories"), list):
                for category in entity["categories"]:
                    if isinstance(category, str) and category not in allowed_categories:
                        errors.append(f"{source_id}.categories: {category!r} is not registered in meta.categories")
            if isinstance(entity.get("sources"), list):
                for value in entity["sources"]:
                    if isinstance(value, str) and value not in allowed_provenance:
                        errors.append(f"{source_id}.sources: {value!r} is not registered in meta.provenance")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=ROOT / "security_feeds.yaml")
    parser.add_argument("--schema", type=Path, default=ROOT / "schema/security-feeds.schema.json")
    parser.add_argument("--readme", type=Path, default=ROOT / "README.md")
    parser.add_argument("--skip-readme-check", action="store_true")
    args = parser.parse_args()
    try:
        data = load_dataset(args.data)
    except Exception as exc:
        print(f"ERROR: cannot parse {args.data}: {exc}", file=sys.stderr)
        return 1
    try:
        import json
        schema = json.loads(args.schema.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"ERROR: cannot load schema {args.schema}: {exc}", file=sys.stderr)
        return 1
    errors, warnings = validate_data(data, schema)
    if not args.skip_readme_check:
        try:
            readme = args.readme.read_text(encoding="utf-8")
            expected = render_directory(data)
            if expected not in readme:
                errors.append("README.md: generated directory is out of date; run `python3 scripts/generate_readme.py`")
        except Exception as exc:
            errors.append(f"README.md: cannot verify generated directory ({exc}); fix dataset validation errors first")
    for warning in warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        print(f"Validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"Validation passed: {len(data.get('entities', []))} source(s), {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
