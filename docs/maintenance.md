# Maintenance policy

## Verification

`status: verified` records a maintainer's evidence that the publisher, website, feed URL, and declared format were checked. Store the check date in `last_verified` using `YYYY-MM-DD`. Automated polling does not update this date. Verification is time-bound evidence, not a guarantee that the endpoint still works.

Automated feed reports use `healthy`, `degraded`, `inconclusive`, and `broken` operational states. A single failed request never changes the curated record. Check 403 and 429 responses, TLS/DNS errors, timeouts, and server errors manually or later from a permitted network. Recheck confirmed failures before proposing a data change.

## Feed checks

Run `python3 scripts/check_feeds.py --output feed-health.json` to check the canonical list. The checker is sequential, rate-limited per repeated domain, uses a finite timeout and response-size bound, follows only HTTP(S) redirects without HTTPS downgrade, and parses XML without executing it. It does not bypass access restrictions. The JSON report may be summarized with `python3 scripts/report_health.py feed-health.json`. Do not commit reports unless they are necessary and contain no unnecessary operational detail.

## Reviews and stale records

Review duplicate URL warnings, but do not merge based on names or domains alone. Assess publisher identity, editorial purpose, and feed content before proposing a merge. Keep disputed records under review while evidence is gathered. Prefer a correction over removal when an official feed has moved. Record material removals or taxonomy decisions in the pull request and changelog.

## GitHub Actions

`validate-data.yml` validates pull requests and default-branch pushes. `check-feeds.yml` runs weekly or manually and stores a short-lived workflow artifact; it does not commit status changes. `generate-readme.yml` checks generated README synchronization in CI. Workflows use minimal read permissions and pin third-party actions to reviewed commit SHAs. Maintainers should review pinned action updates deliberately.

To enable scheduled checks, ensure Actions are enabled for the repository and workflow permissions permit read-only checkout and artifact upload. Manual runs are available from the Actions tab. No secrets are required.
