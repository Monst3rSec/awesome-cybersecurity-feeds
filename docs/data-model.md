# Data model

`security_feeds.yaml` is the sole canonical dataset. `schema/security-feeds.schema.json` defines field types, allowed identifiers, URL and date formats, and rejects unknown keys. The validator adds cross-record checks that JSON Schema does not express.

## Top-level fields

- `meta.schema_version`: integer version of the dataset structure.
- `meta.description`: short scope statement.
- `meta.categories`: registered category IDs, names, and descriptions.
- `meta.provenance`: supported source provenance identifiers.
- `meta.imported_metadata`: snapshot of the source file's title, generation date, entity/category counts, category descriptions, and notes. It preserves the supplied dataset metadata; current counts are computed from `entities` during review.
- `entities`: list of source records.

## Entity fields

Each entity requires `id`, `name`, `website`, `feed.url`, `feed.format`, `categories`, `sources`, and `status`. IDs are stable kebab-case identifiers. URLs must use HTTP or HTTPS. Formats are `rss`, `atom`, or `rdf`. Each record can use multiple category identifiers.

`sources` preserves the source/provenance identifiers supplied with the existing collection: `ai-soc-vendor-directory` and `threat-feed-collection`. They identify collection origins, not editorial trust or endorsement. Add a new identifier only through a reviewed schema and data-model change. `status` is a curation marker: `unverified`, `verified`, `needs_review`, or `deprecated`. A verified record must include `last_verified` as an ISO 8601 date. `latest_post_seen` is also an ISO 8601 date. Optional fields include `description`, `publisher`, `notes`, `last_verified`, and `latest_post_seen`.

Duplicate feed and website URLs are warnings for human review. They do not cause automatic merging. Automated health results are separate report artifacts and never change this dataset.

## Unknown fields and schema changes

Unknown fields are validation errors so typos cannot silently become undocumented data. To add a field, update the JSON Schema, this document, the template if relevant, validation tests, and any README or CI behavior that depends on it. Keep optional fields optional unless a deliberate versioned migration is approved.
