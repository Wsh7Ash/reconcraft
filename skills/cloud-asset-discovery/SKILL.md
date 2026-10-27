---
name: cloud-asset-discovery
description: "Identify cloud services the application depends on from public naming, headers and configuration, and keep them scope-separated. Use when responses reference storage buckets, serverless endpoints or platform services that sit outside the application's own hosts"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [cloud, assets, scope]
---

# Cloud Asset Discovery

> Identify cloud services the application depends on from public naming, headers and configuration, and keep them scope-separated

**Use when:** responses reference storage buckets, serverless endpoints or platform services that sit outside the application's own hosts

**Avoid when:** the entire estate runs on infrastructure the program explicitly lists as its own

## Procedure

1. Collect cloud indicators from responses and clients: storage bucket URLs, function endpoints, CDN hostnames and platform headers.
2. Determine whether each referenced resource belongs to the vendor's account, using only public evidence such as naming and responses.
3. Separate public-read assets from private ones, since exposure differs and so does report wording.
4. Check each discovered resource for listing or misconfiguration ONLY where the program authorizes testing it.
5. Mark third-party-owned resources as dependencies rather than targets, so they never enter an automated scan list.
6. Record everything in inventory with provider, ownership evidence and scope status.

## Signals

- A response references a storage bucket URL directly, which is an asset class most crawlers never enumerate.
- Function or serverless endpoints appear with platform hostnames that no DNS query would surface.
- Platform headers reveal the provider account or region handling the request.
- A bucket name follows vendor naming yet is absent from the program's published asset list.

## Patterns

**1. Indicator row**

```text
resource=bucket storage-provider endpoint class=storage evidence=response-url ownership=likely-vendor scope=unlisted
```

**2. Ownership**

```text
naming matches vendor + vendor docs reference it -> likely vendor
shared or unrelated naming -> third-party, dependency only
```

**3. Report wording**

```text
public listing observed on vendor-owned storage -> finding
resource owned by provider -> dependency note, not a finding against the vendor
```

## Pitfalls

- Testing a bucket or function that belongs to another tenant because its name merely looked familiar.
- Reporting provider-side defaults as vendor misconfiguration without proving the resource is the vendor's.
- Skipping cloud assets entirely because your crawl never surfaced them, leaving a whole asset class unreviewed.

## Done when

- Every referenced cloud resource has ownership evidence, scope status and a public/private classification.
- Third-party resources are stored as dependencies and excluded from any list your tools scan automatically.

## References

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [OWASP - cloud security resources](https://owasp.org/)
