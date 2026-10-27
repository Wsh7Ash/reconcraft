---
name: virtual-host-enumeration
description: "Discover web applications that share one address by varying Host headers and hostname routing within your authorized scope. Use when one in-scope address serves multiple applications, or you suspect admin, staging and API vhosts answer on an existing host"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [vhost, web, enumeration]
---

# Virtual Host Enumeration

> Discover web applications that share one address by varying Host headers and hostname routing within your authorized scope

**Use when:** one in-scope address serves multiple applications, or you suspect admin, staging and API vhosts answer on an existing host

**Avoid when:** each application has its own dedicated hostname already documented in your inventory

## Procedure

1. Confirm which address and hostname are in scope, since a vhost probe still sends requests to the host you name.
2. Collect candidate names from DNS, certificate SANs, archive data and your permutation work rather than guessing from nothing.
3. Send requests with the candidate Host header while keeping the connection target fixed, at a rate that matches your ceiling.
4. Compare each response against a baseline for the default vhost: status, length, title and a content hash all matter.
5. Group hits by application type so an admin interface and a marketing site do not end up in the same bucket.
6. Add discovered vhosts to inventory with their discovery method, then re-run only the delta on future passes.

## Signals

- A candidate Host produces a different title or content hash than the default vhost baseline.
- Content length, status code and redirect target all shift together, which is a strong vhost signal rather than noise.
- A vhost returns an application login page that no public hostname serves.
- The default vhost answers identically for unknown names, which means your baseline must come from a known-good host.

## Patterns

**1. Baseline**

```text
Host: unknown-random.invalid -> 404, len=1243, hash=9f3a...
Host: app.example.com       -> 200, len=48210, hash=11bc...  DIFF
```

**2. Probe set**

```text
candidates: admin, api, staging, old, mail, vpn, build, cdn
carried from: dns + crt.sh + permutations, not random dictionary blasting
```

**3. Hit record**

```text
ip=203.0.113.10 vhost=admin.example.com method=host-header status=200 app=admin-console
```

## Pitfalls

- Using a random unknown host as the baseline when the server default page differs from every real vhost, producing false hits.
- Probing with names you invented instead of sourced candidates, which multiplies requests without adding coverage.
- Forgetting that a CDN in front of the address may answer any Host with the same edge page and hide the real vhost.

## Done when

- Each discovered vhost differs from the baseline on at least two independent response properties.
- New vhosts are recorded in inventory with discovery method, and unconfirmed candidates are excluded from later phases.

## References

- [OWASP Web Security Testing Guide - information gathering](https://owasp.org/www-project-web-security-testing-guide/)
- [RFC 9110 - Host routing semantics](https://www.rfc-editor.org/rfc/rfc9110)
