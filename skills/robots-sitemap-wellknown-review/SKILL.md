---
name: robots-sitemap-wellknown-review
description: "Read the machine-readable files the application publishes, since they routinely advertise administrative paths and registered capabilities. Use when you start reviewing a newly discovered host and want its own published pointers before running any crawler"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [paths, discovery, standards]
---

# Robots, Sitemap and Well-Known Review

> Read the machine-readable files the application publishes, since they routinely advertise administrative paths and registered capabilities

**Use when:** you start reviewing a newly discovered host and want its own published pointers before running any crawler

**Avoid when:** you already crawled and diffed these files in a recent run and nothing has changed since

## Procedure

1. Fetch robots.txt and sitemap files directly from each in-scope host rather than assuming one host's copy applies to another.
2. Parse disallow rules as candidate paths, keeping the ones that point at application areas instead than crawler noise.
3. Walk every sitemap index recursively and collect URLs that never appear in the navigable interface.
4. Enumerate the well-known directory for registered capabilities such as single sign-on, security.txt and asset metadata.
5. Classify each discovery as documented (intended to be public), adjacent (publishable but unlinked) or sensitive-looking.
6. Add the paths to your content-discovery candidate set so later passes confirm status, auth requirements and behavior.

## Signals

- robots.txt disallows an admin or export path that is not linked anywhere in the application.
- A sitemap references a legacy or versioned host that is absent from your inventory.
- The well-known directory reveals an identity provider, indicating single sign-on integration worth mapping.
- security.txt lists a contact or policy that clarifies the program's disclosure channel.

## Patterns

**1. robots parse**

```text
User-agent: *
Disallow: /admin/
Disallow: /export/all
Disallow: /internal/v2/   -> candidates, not permission
```

**2. well-known set**

```text
/.well-known/security.txt
/.well-known/openid-configuration
/.well-known/assetlinks.json
/.well-known/change-password
```

**3. Classification**

```text
documented  -> already public, note for coverage
adjacent    -> add to discovery queue
sensitive   -> validate carefully and scope-check first
```

## Pitfalls

- Treating disallow rules as forbidden zones to avoid; for a tester they are hints, not access control.
- Reading robots.txt only at the apex and missing per-host differences across subdomains.
- Requesting every well-known path on hosts where the scheme is irrelevant, which burns rate budget for nothing.

## Done when

- Every in-scope host's robots, sitemap and relevant well-known files are fetched, parsed and classified.
- New paths are queued in the discovery pipeline with scope confirmed, and the files are kept for later diffing.

## References

- [robots.txt specification](https://www.robotstxt.org/)
- [sitemaps.org protocol](https://www.sitemaps.org/)
