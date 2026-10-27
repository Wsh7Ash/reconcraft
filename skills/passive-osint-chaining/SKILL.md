---
name: passive-osint-chaining
description: "Combine public sources into one picture of the target organization without ever contacting the vendor's systems. Use when you are in the earliest recon phase, active testing is paused, or you need context that DNS and certificates cannot provide"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [osint, passive, recon]
---

# Passive OSINT Chaining

> Combine public sources into one picture of the target organization without ever contacting the vendor's systems

**Use when:** you are in the earliest recon phase, active testing is paused, or you need context that DNS and certificates cannot provide

**Avoid when:** you already have complete coverage from DNS and certificate data and only need to refresh what changed

## Procedure

1. Start from organization identity: official domains, subsidiaries, acquisitions and product names, since each is a separate asset family.
2. Harvest references to those names from code repositories, package metadata, documentation and archived pages.
3. Collect developer-facing artifacts such as job postings and status pages, which frequently name internal tooling and platforms.
4. Record every lead with its source URL and capture date so you can re-check it when the disclosure conversation starts.
5. Separate leads into in-scope hosts, unlisted-but-plausible assets and clearly unrelated mentions before any active work.
6. Keep the collection passive: query public datasets and archives, never the vendor's own servers.

## Signals

- A job posting names an internal platform hostname that appears nowhere in DNS or certificate data.
- Public code repositories reference environment variables and endpoints belonging to the vendor's applications.
- An archived page links to a customer portal or admin host that has since been removed from navigation.
- A subsidiary or acquired brand runs software that shares authentication with the main platform.

## Patterns

**1. Lead record**

```text
lead=ci.internal.example.com source=job-posting url=https://... captured=2026-10-27 class=unlisted
```

**2. Source tiers**

```text
tier 1: vendor's own published pages and repositories
tier 2: archives, package registries, public datasets
tier 3: third-party mentions - verify before believing
```

**3. Classification**

```text
in-scope   -> queue for validation
unlisted   -> ask the program before testing
unrelated  -> keep in notes only, never in the asset inventory
```

## Pitfalls

- Pulling personal information about employees into your notes, which is unnecessary for a technical finding and creates privacy risk.
- Treating a third-party mention as confirmed ownership without a second source.
- Drifting into active probing because a dataset offers an easy test button; passive means no packets to the vendor.

## Done when

- Every lead carries a source, capture date and scope classification before any active testing uses it.
- The collection contains no personal data beyond what is needed to identify the asset, and no vendor servers were contacted.

## References

- [HackerOne - reconnaissance resources](https://hackerone.com/blog)
- [Internet Archive - Wayback Machine](https://web.archive.org/)
