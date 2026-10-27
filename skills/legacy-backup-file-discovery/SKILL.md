---
name: legacy-backup-file-discovery
description: "Check whether the application serves exposed copies, archives or editor leftovers of its own files within your authorized scope. Use when a host serves versioned or templated files and you want to know whether backups or swap files are publicly reachable"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [files, backup, exposure]
---

# Legacy Backup File Discovery

> Check whether the application serves exposed copies, archives or editor leftovers of its own files within your authorized scope

**Use when:** a host serves versioned or templated files and you want to know whether backups or swap files are publicly reachable

**Avoid when:** the asset is a third-party CDN endpoint where file requests do not reach vendor-controlled storage

## Procedure

1. Inventory actual file paths from your crawl: scripts, configuration, exports and downloadable documents already in use.
2. Derive backup naming variants from those real paths, since guessing from nothing produces noise while deriving produces leads.
3. Request each variant once at your normal rate and compare against a known-missing response to filter soft-404s.
4. Confirm a hit by checking content type, size and an actual file signature inside the body rather than trusting status alone.
5. If an archive is served, download it locally and inspect it there instead of repeatedly fetching it from the target.
6. Report exposure through the program channel with the affected path and contents summary, redacting any real secrets you find.

## Signals

- A candidate returns a content type such as application/zip or application/x-tar instead of the site's normal HTML.
- Response size matches a plausible archive rather than your missing-page baseline length.
- An editor swap or temporary file contains original source that the public application does not serve.
- A configuration-shaped file contains keys or internal hostnames, which you should report without publishing values.

## Patterns

**1. Variant set**

```text
app.js -> app.js.bak, app.js~, app.js.old, .app.js.swp
config.yml -> config.yml.bak, config.yml~, config.yml.save
```

**2. Content confirmation**

```text
status=200 AND type=application/zip AND magic bytes PK\x03\x04 -> real archive
status=200 AND type=text/html AND len==missing-baseline -> soft-404, discard
```

**3. Safe handling**

```text
fetch once, save locally, inspect offline, redact values before writing anything into a report
```

## Pitfalls

- Requesting hundreds of variants per file, which inflates traffic and breaks the rate ceiling for marginal coverage.
- Confusing an application's custom error page, served with status 200, for a discovered backup.
- Pasting discovered secret values verbatim into a report, which spreads the secret instead of getting it rotated.

## Done when

- Every claimed exposure was confirmed by content type plus an in-body signature, not by status code alone.
- Files were fetched once and analyzed locally, and any secret material is described rather than reproduced in the report.

## References

- [OWASP Web Security Testing Guide - information gathering](https://owasp.org/www-project-web-security-testing-guide/)
- [PayloadsAllTheThings - file disclosure resources](https://github.com/swisskyrepo/PayloadsAllTheThings)
