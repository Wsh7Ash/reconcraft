---
name: favicon-hash-infra-fingerprint
description: "Use stable asset hashes to cluster hosts that run the same application across your inventory and public datasets. Use when you have many hosts and want to group those serving the same software or find siblings with identical deployments"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [fingerprint, clustering, assets]
---

# Favicon and Asset Hash Fingerprinting

> Use stable asset hashes to cluster hosts that run the same application across your inventory and public datasets

**Use when:** you have many hosts and want to group those serving the same software or find siblings with identical deployments

**Avoid when:** the inventory is small enough to compare directly, where hashing adds work without adding insight

## Procedure

1. Fetch each host's favicon and other stable assets once, recording the source URL and response metadata.
2. Compute a content hash over the raw bytes so identical assets across hosts produce identical values.
3. Cluster hosts by hash to find groups that clearly share a deployment, template or platform.
4. Sample one host per cluster and confirm the shared fingerprint means shared software rather than a shared default file.
5. Compare clusters against your asset inventory to find unlisted hosts that serve the vendor's own template.
6. Store hashes with fetch dates so asset rotation shows up as a cluster change rather than a surprise.

## Signals

- Several hosts share a hash but appear on unrelated domains, which usually means a default or vendor-supplied asset.
- An unlisted host's hash matches a cluster of known vendor hosts, which is a strong ownership signal.
- A host's hash changes with no code release on your side, hinting at a redeployment or configuration change.
- One cluster contains a host that returns a different application entirely, showing shared hosting rather than shared software.

## Patterns

**1. Hash record**

```text
host=app.example.com asset=/favicon.ico sha256=9f3a... size=15406 captured=2026-10-27
```

**2. Cluster grouping**

```text
hash 9f3a -> [app.example.com, portal.example.com, 203.0.113.10]
-> same deployment family, confirm with one manual review
```

**3. Ownership signal**

```text
unlisted host hash matches vendor cluster -> candidate vendor asset -> scope question
```

## Pitfalls

- Hashing a placeholder image served by a default page, which clusters every unknown host together meaninglessly.
- Forgetting to hash raw bytes, so compression or re-encoding differences break every comparison.
- Assuming a shared hash proves shared ownership when many platforms ship an identical default asset.

## Done when

- Each cluster is documented with its members, hash and capture date, and sampled for a real shared-software check.
- Unlisted hosts matching a vendor cluster are queued as scope questions rather than tested directly.

## References

- [Shodan - favicon hashing concepts](https://www.shodan.io/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
