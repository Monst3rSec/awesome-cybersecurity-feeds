# Contributing

Thank you for helping maintain this directory. Contributions are reviewed as data changes; maintainers may ask for evidence, edits, or clarification before merging.

## Add or update a source

1. Search `security_feeds.yaml` and the README for the source name, website, and feed URL.
2. Check the publisher's official website and confirm that the feed URL is publicly linked or otherwise supported by clear evidence. Do not bypass authentication, anti-bot controls, or access restrictions.
3. Choose the best existing category in [docs/categories.md](docs/categories.md). Propose a new category through the category issue form rather than adding a new identifier directly.
4. Add or update a record in `security_feeds.yaml`, using a stable, lowercase kebab-case ID. Copy [templates/source-template.yml](templates/source-template.yml). Preserve multiple relevant categories.
5. Preserve the applicable registered `sources` provenance identifier. The current IDs are `ai-soc-vendor-directory` and `threat-feed-collection`; propose a new ID with evidence rather than adding one silently. Do not imply independent research for vendor material.
6. Use `status: unverified` unless a maintainer has checked the source under the policy in [docs/maintenance.md](docs/maintenance.md). Never invent a verification date. Descriptions must be neutral and factual. Mention mostly promotional material in `notes` where useful.
7. Install dependencies, validate, and regenerate the directory:

   ```sh
   python3 -m pip install -r requirements.txt
   python3 scripts/validate_sources.py
   python3 scripts/generate_readme.py
   python3 scripts/validate_sources.py
   ```

8. Submit a pull request using the checklist. Include evidence for the feed and explain any corrections or category choice.

## Quality and safety standards

- Sources must be materially relevant to cybersecurity.
- Prefer official feeds when available; identify third-party feed hosting accurately.
- Avoid duplicates. Similar names or shared domains are review signals, not grounds to merge records automatically.
- Do not add credentials, API keys, private information, or URLs intended to deliver malware. Do not include tracking or session tokens in URLs.
- Recheck broken feeds before suggesting removal. A single automated failure is not enough to remove a record or change its curation status.
- Keep optional fields empty when evidence is unavailable; do not fabricate details.

## Review and disputes

Maintainers compare records by URL, publisher, and source purpose, then ask contributors to resolve likely duplicates. Stale entries are rechecked using the documented verification policy. Category disagreements are resolved against the current registry; taxonomy changes require a documented proposal and coordinated schema, data, README, and test changes. Disputed sources are assessed for relevance, evidence, and neutral description, with the rationale recorded in the review or change history. See [maintenance policy](docs/maintenance.md).

## Licensing

The repository's scripts and documentation are provided under the [MIT License](LICENSE). A contribution of directory metadata does not grant rights to third-party publisher content. Contributors should submit links and factual metadata, not copied articles or feed contents.
