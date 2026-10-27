---
name: asn-netblock-attribution
description: "Map the vendor's autonomous systems and announced prefixes to find infrastructure that never appears in DNS or on the scope page. Use when a program exposes only a few hostnames and you suspect more infrastructure exists under the organization's own network allocations"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [asn, netblock, infrastructure]
---

# ASN and Netblock Attribution

> Map the vendor's autonomous systems and announced prefixes to find infrastructure that never appears in DNS or on the scope page

**Use when:** a program exposes only a few hostnames and you suspect more infrastructure exists under the organization's own network allocations

**Avoid when:** the program supplies a complete asset inventory and its network range matches what DNS already revealed

## Procedure

1. Identify the organization's autonomous systems through public routing data and confirm which ones still announce prefixes today.
2. List the prefixes each system announces and separate the vendor's own space from customer or transit allocations.
3. Cross-check the range against the addresses your DNS work already produced, which validates both datasets at once.
4. Look for reverse names and certificates inside the vendor's space to find hosts with no DNS entry at all.
5. Exclude infrastructure belonging to upstream providers, since transit space is never the target you are authorized to test.
6. Save the confirmed ranges and their announcement dates so routing changes show up as diffs in later runs.

## Signals

- A prefix announced by the vendor contains hosts that never appear in certificate logs or DNS datasets.
- Routing data shows a recently announced prefix with no corresponding entry in your inventory.
- Reverse names inside the range reveal environments such as build, staging or vpn that are absent from public DNS.
- A prefix previously attributed to the vendor is now announced by a different organization, meaning ownership moved.

## Patterns

**1. Range record**

```text
org=Example Corp asn=64500 prefix=203.0.113.0/24 announced=2024-06 source=rpki-validated-routing-data
```

**2. Coverage check**

```text
dns addresses found: 6    range size: 256    reverse names in range: 14
-> 8 addresses are not yet in inventory, enumerate them
```

**3. Exclusion**

```text
transit or upstream provider prefix -> mark third-party, never scan
```

## Pitfalls

- Scanning an entire announced prefix when only a handful of addresses belong to the target application.
- Confusing the hosting provider's autonomous system with the vendor's own, which leads to testing shared infrastructure.
- Ignoring that ownership changes over time; stale range data silently authorizes traffic against someone else.

## Done when

- Confirmed ranges are backed by current routing data and cross-checked against your DNS results.
- Every address you plan to test maps to vendor-owned space, and third-party or transit ranges are excluded explicitly.

## References

- [RIPE routing documentation](https://www.ripe.net/)
- [HackTricks - infrastructure enumeration](https://book.hacktricks.xyz/)
