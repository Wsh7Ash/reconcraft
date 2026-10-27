---
name: passive-subdomain-discovery
description: "Grow a subdomain list from public datasets, certificate logs and archives without sending a single packet to the target. Use when you are at the start of recon, the program forbids aggressive scanning, or you want candidate hosts before touching the target at all"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [subdomains, osint, passive]
---

# Passive Subdomain Discovery

> Grow a subdomain list from public datasets, certificate logs and archives without sending a single packet to the target

**Use when:** you are at the start of recon, the program forbids aggressive scanning, or you want candidate hosts before touching the target at all

**Avoid when:** you already hold a complete inventory from a prior run and only need to check what changed since then

## Procedure

1. Query certificate transparency logs for every registered domain and collect all subject alternative names, including wildcard entries.
2. Pull historical DNS and archive data to recover subdomains that no longer resolve but still appear in old application links.
3. Query public DNS datasets and search indexes for hostnames referenced in JavaScript, mobile app configs or documentation pages.
4. Dedupe everything into a single candidate list, keeping the first-seen source next to each hostname for later ownership checks.
5. Separate candidates into resolves-now and did-not-resolve-so-far, because dead names are takeover leads while live names are test surface.
6. Save the candidate list as a snapshot so tomorrow's query can be diffed against it instead of merged blindly.

## Signals

- A certificate SAN list contains hostnames that never appear on the program's scope page or in DNS answers.
- Archived copies of the site reference admin, staging or legacy hosts that are absent from current crawls.
- A wildcard DNS answer makes every random label resolve, which means DNS alone cannot confirm a hostname exists.
- A previously resolving hostname stops answering, which is a candidate for dangling-resource review rather than deletion.

## Patterns

**1. CT query shape**

```text
crt.sh?%.example.com -> name_value rows, dedupe, strip wildcards, lowercase
source=crt.sh first_seen=2026-03-14 host=api-v2.example.com
```

**2. Snapshot diff**

```text
new:     staging.example.com
removed: legacy.example.com
same:    214 hosts
-> investigate 'new' first
```

**3. Two-bucket split**

```text
resolving   -> active validation phase
non-resolving -> dangling resource phase (verify, never claim blindly)
```

## Pitfalls

- Trusting a hostname from one dataset without a second source, which floods your list with typos and stale names.
- Assuming a wildcard answer proves a subdomain exists; generate random labels first to learn whether wildcarding is on.
- Skipping the snapshot, so the next run cannot tell you which hosts are genuinely new.

## Done when

- You have a deduplicated candidate list with a source per hostname and a resolving/non-resolving split.
- The list is stored as a dated snapshot that a later run can diff without re-querying everything from scratch.

## References

- [Certificate Transparency - overview](https://en.wikipedia.org/wiki/Certificate_Transparency)
- [crt.sh certificate search](https://crt.sh/)
