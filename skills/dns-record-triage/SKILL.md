---
name: dns-record-triage
description: "Read the full record set of every in-scope zone to learn where mail, redirects and services actually point before any HTTP work begins. Use when you hold a hostname list and want to understand its infrastructure and find records that expose additional surface"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [dns, records, triage]
---

# DNS Record Triage

> Read the full record set of every in-scope zone to learn where mail, redirects and services actually point before any HTTP work begins

**Use when:** you hold a hostname list and want to understand its infrastructure and find records that expose additional surface

**Avoid when:** a single host has already been fully mapped and you only need to re-check whether its address changed

## Procedure

1. Collect the common record types for each zone: address, name, mail, text, service and any delegation records.
2. Follow CNAME chains to their end, because the terminal name reveals the actual provider serving the host.
3. Read SPF and DMARC text records for mail policy and for include chains that name additional vendor domains.
4. Note nameservers and zone delegations, which expose subzone boundaries and the DNS provider in use.
5. Flag records that point at third-party platforms, since those hosts are usually out of scope even when the name looks internal.
6. Store the collected records as a dated snapshot so TTL and provider changes become visible over time.

## Signals

- A CNAME terminates at a cloud or SaaS provider the program never mentioned in its scope description.
- SPF includes reveal mail vendors and internal senders that are additional infrastructure to inventory.
- The zone delegates a subzone to different nameservers, which often means a separate application lives there.
- Address records use documentation ranges or private space, which usually means split-horizon DNS rather than public surface.

## Patterns

**1. Record sweep**

```text
example.com A/AAAA  -> edge addresses
www CNAME -> shop.provider.net (third party)
example.com MX 10 mail.example.com
example.com TXT "v=spf1 include:_spf.mailvendor.net -all"
```

**2. CNAME chain**

```text
app.example.com -> app.cdn.net -> cluster7.edge.net
terminal provider = where the host is really served
```

**3. Snapshot row**

```text
name | type | value | ttl | provider_hint | first_seen
www.example.com CNAME shop.provider.net 300 s3-shop 2026-10-27
```

## Pitfalls

- Checking only address records and missing names that reveal mail, subzone delegation and third-party routing.
- Stopping the CNAME chain at the first hop and misattributing the true hosting provider.
- Forgetting TTL when diffing, so routine DNS maintenance looks like an infrastructure change worth investigating.

## Done when

- Every in-scope zone has a full record snapshot with CNAME chains followed to their terminal provider.
- Third-party endpoints found through records are marked out of scope in your inventory rather than queued for testing.

## References

- [RFC 1035 - DNS implementation and resource records](https://www.rfc-editor.org/rfc/rfc1035)
- [SPF receiver guidance](https://www.rfc-editor.org/rfc/rfc7208)
