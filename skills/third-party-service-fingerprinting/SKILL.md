---
name: third-party-service-fingerprinting
description: "Identify the external services an application depends on so you know what is yours to test and what belongs to someone else. Use when an application pulls in external scripts, widgets, payment flows or identity providers that affect your test surface"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [third-party, supply-chain, fingerprint]
---

# Third-Party Service Fingerprinting

> Identify the external services an application depends on so you know what is yours to test and what belongs to someone else

**Use when:** an application pulls in external scripts, widgets, payment flows or identity providers that affect your test surface

**Avoid when:** the application is fully self-hosted with no external dependencies in its responses

## Procedure

1. Collect external references from responses: scripts, frames, images, stylesheets, beacons and API calls made by clients.
2. Group them by provider and by role: analytics, identity, payments, content delivery, support and messaging.
3. Determine which providers are loaded with elevated privilege, such as identity or payment scripts that see sensitive context.
4. Mark each provider domain as out of scope unless the program explicitly includes it, so no request accidentally targets it.
5. Record integration points where vendor code and provider code exchange data, since those seams are where misconfiguration shows up.
6. Keep the dependency list current, because providers change on every deployment without any change to the vendor's own code.

## Signals

- A provider script loads with full access to the page context, which is a supply-chain risk worth documenting.
- An identity provider integration reveals the sign-in flow and any custom claims your tests should respect.
- A script is loaded over a different scheme than the page, which is a mixed-content and integrity concern.
- A previously observed provider disappears, indicating a migration that changes your dependency map.

## Patterns

**1. Dependency row**

```text
provider=identity.example.net role=login privilege=high scope=third-party
provider=analytics.example.org role=telemetry privilege=page scope=third-party
```

**2. Integrity check**

```text
script src=https://cdn.example.com/lib.js integrity=absent crossorigin=use-credentials
-> note integrity posture in your review
```

**3. Scope rule**

```text
third-party host -> never test directly; report integration risk to the vendor instead
```

## Pitfalls

- Testing a third-party provider because it appears in your crawl, which is outside your authorization.
- Missing a late-loading provider that only appears after interaction, so your dependency map is incomplete.
- Listing providers without recording privilege level, which hides the difference between a widget and an identity provider.

## Done when

- Every external dependency is grouped by provider, role and privilege, with scope status recorded.
- No request in your test plan targets a provider host, and high-privilege integrations are flagged for review.

## References

- [OWASP - software supply chain guidance](https://owasp.org/)
- [MDN - subresource integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)
