---
name: dangling-cname-candidates
description: "Identify hostnames that still point at decommissioned third-party resources so you can report a takeover risk without touching anyone else's tenant. Use when a DNS record in scope CNAMEs to a provider you can verify the vendor no longer controls, and you need to confirm the risk safely"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [takeover, dns, risk]
---

# Dangling CNAME Candidates

> Identify hostnames that still point at decommissioned third-party resources so you can report a takeover risk without touching anyone else's tenant

**Use when:** a DNS record in scope CNAMEs to a provider you can verify the vendor no longer controls, and you need to confirm the risk safely

**Avoid when:** the resource still resolves to a live vendor configuration, or the hostname belongs to a third party outside program scope

## Procedure

1. Find in-scope records whose CNAME or alias terminates at a known provider platform rather than at vendor-owned infrastructure.
2. Check whether the referenced resource still exists in the provider's system, using only information the provider exposes publicly.
3. Distinguish three states: active and owned, inactive but claimed, and inactive and claimable, because only the last is a real risk.
4. Use the provider's own public lookup or documentation to confirm absence, never by claiming or reserving the resource yourself.
5. Document the chain from in-scope hostname to provider resource with timestamps, since providers re-provision resources frequently.
6. Report the condition with the remediation of deleting the stale record, and re-verify before disclosure in case the state changed.

## Signals

- A CNAME terminates at a platform hostname while the vendor's own application never references that host.
- The provider's public lookup reports the resource as not found, which is the standard dangling indicator.
- The record appeared during a migration and was never cleaned up, visible in your dated DNS snapshots.
- Similar hosts in the same zone resolve normally while one specific name consistently fails at the provider edge.

## Patterns

**1. Chain record**

```text
old.example.com CNAME site.storage-provider.net
lookup: resource not found on provider
dating: record first seen 2025-11, vendor app references: none
```

**2. State table**

```text
active    -> resource answers, owner confirmed      -> no issue
inactive+claimed -> provider shows existing config  -> informational
inactive+unclaimed -> provider shows no resource    -> reportable dangling reference
```

**3. Safe check**

```text
public lookup only, no claim, no reservation, no configuration change on any system
```

## Pitfalls

- Claiming a resource to prove a finding, which touches infrastructure you do not own and violates most program rules.
- Reporting a dangling record without re-checking, because providers and vendors often fix these within days.
- Missing a provider that serves an existing resource from the same hostname, turning a false positive into a wasted report.

## Done when

- Each candidate is classified as active, inactive-claimed or inactive-unclaimed with the public evidence recorded.
- No action you took altered any third-party system, and the finding was re-verified immediately before disclosure.

## References

- [HackTricks - Subdomain takeover concepts](https://book.hacktricks.xyz/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
