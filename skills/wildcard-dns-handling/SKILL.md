---
name: wildcard-dns-handling
description: "Detect wildcard and catch-all DNS responses early and filter them out so enumeration results stay honest. Use when any subdomain enumeration runs against a domain, especially one hosted on a cloud or CDN provider that commonly enables wildcards"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [dns, wildcard, validation]
---

# Wildcard DNS Handling

> Detect wildcard and catch-all DNS responses early and filter them out so enumeration results stay honest

**Use when:** any subdomain enumeration runs against a domain, especially one hosted on a cloud or CDN provider that commonly enables wildcards

**Avoid when:** you are only reading published DNS records and never generating candidate names

## Procedure

1. Query several random labels at the parent domain and compare the answers to decide whether a wildcard or catch-all is present.
2. Distinguish a true wildcard record from a catch-all resolver that answers unknown names with the same server address.
3. Check both the apex and any delegated subzones, since wildcarding differs per zone and a parent wildcard does not imply a child one.
4. Record the wildcard answer set so candidate results can be filtered by comparison rather than by assumption.
5. For wildcarded zones, keep only answers that differ from the recorded wildcard set or that resolve through a distinct CNAME.
6. Re-test wildcard status when results suddenly spike, because a migration to a new DNS provider often turns wildcarding on.

## Signals

- Random labels like a1b2c3.domain.tld answer with real addresses instead of NXDOMAIN.
- Every candidate in a large wordlist resolves to one identical address set, a classic wildcard signature.
- A zone recently moved to a new DNS host and now answers names that did not exist yesterday.
- Wildcard answers differ from the certificate's SAN set, which lets you separate DNS wildcarding from cert wildcarding.

## Patterns

**1. Detection**

```text
probe a1b2c3.domain.tld -> 198.51.100.7
probe q7w8e9.domain.tld -> 198.51.100.7
identical answers on random labels = wildcard present
```

**2. Filter rule**

```text
candidate resolves to wildcard set AND cname identical -> discard
candidate resolves to distinct address or unique cname  -> keep
```

**3. Zone note**

```text
domain.tld           wildcard=no
*.staging.domain.tld  wildcard=yes (filter required)
```

## Pitfalls

- Reporting every wordlist hit on a wildcarded zone as a discovered subdomain, which destroys your credibility with triage.
- Testing wildcard only at the apex and missing delegated zones that behave differently.
- Confusing a wildcard DNS record with a wildcard certificate; they are independent and both need separate checks.

## Done when

- Wildcard status is documented for each zone and filtering is applied to every enumeration result you keep.
- A rerun with fresh random probes reproduces the same wildcard verdict, confirming the filter still matches reality.

## References

- [HackTricks - DNS pentesting](https://book.hacktricks.xyz/)
- [RFC 4592 - DNS wildcard semantics](https://www.rfc-editor.org/rfc/rfc4592)
