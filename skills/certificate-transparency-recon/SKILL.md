---
name: certificate-transparency-recon
description: "Mine public certificate logs for hostnames, issuers and renewal patterns that reveal infrastructure you have not seen elsewhere. Use when you need hostnames beyond what DNS and archives provide, or want to track when new certificates appear for a domain"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [certificates, osint, subdomains]
---

# Certificate Transparency Recon

> Mine public certificate logs for hostnames, issuers and renewal patterns that reveal infrastructure you have not seen elsewhere

**Use when:** you need hostnames beyond what DNS and archives provide, or want to track when new certificates appear for a domain

**Avoid when:** a program supplies its full asset list and your DNS work already covers every listed domain

## Procedure

1. Query transparency logs for the apex and each registered domain, collecting every subject alternative name in the results.
2. Normalize names: lowercase, strip wildcards, dedupe, and keep the log entry date and issuer for each certificate.
3. Group results by issuer and validity window to spot automated issuance patterns and hosting platforms in use.
4. Separate names that resolve from names that do not, since each group feeds a different later phase.
5. Watch for newly issued certificates and diff them against your baseline, which is often the earliest signal of new infrastructure.
6. Route names that fall outside program scope to confirmation before any request touches them.

## Signals

- A certificate contains internal-looking names such as vpn, jenkins or mail that never appear in public DNS.
- A sudden burst of issuance for one domain suggests a migration or a new environment coming online.
- Issuers differ across name groups, revealing which platform serves which part of the estate.
- An expired certificate still lists a hostname, which is a lead for decommissioned or dangling assets.

## Patterns

**1. Log query**

```text
crt.sh?%.example.com -> rows: name_value, not_before, issuer_ca_id
dedupe on lowercase name, keep earliest and latest seen
```

**2. Grouping**

```text
issuer=Let's Encrypt  names=142  wildcard=yes  cadence=~90d
issuer=Private CA     names=6    internal-looking names present
```

**3. Certificate diff**

```text
new since baseline: staging-v2.example.com (cert issued 2026-10-26) -> investigate
```

## Pitfalls

- Reporting every certificate name as a live host, when many are historical or never resolved at all.
- Ignoring wildcards, which hide the actual hostnames and produce misleading counts.
- Forgetting scope checks on names that look internal, which are precisely the ones you must ask about first.

## Done when

- Certificate names are normalized, grouped by issuer and split into resolving and non-resolving sets.
- New issuance since your baseline is diffed and each new name is scope-checked before use.

## References

- [crt.sh certificate search](https://crt.sh/)
- [Certificate Transparency overview](https://en.wikipedia.org/wiki/Certificate_Transparency)
