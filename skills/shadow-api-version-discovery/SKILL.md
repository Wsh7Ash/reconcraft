---
name: shadow-api-version-discovery
description: "Find API versions and base paths the application still answers on but no longer advertises in its current client. Use when an API exposes version prefixes such as v1, v2 or date-based schemes and you want retired versions still reachable"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [api, versions, shadow]
---

# Shadow API Version Discovery

> Find API versions and base paths the application still answers on but no longer advertises in its current client

**Use when:** an API exposes version prefixes such as v1, v2 or date-based schemes and you want retired versions still reachable

**Avoid when:** the API documents exactly one version and your endpoint inventory already confirms no alternates exist

## Procedure

1. Collect all version markers found so far: URL prefixes, header-based versions, media types and request-body fields.
2. Probe neighbouring version strings on a single known-good operation, keeping the request identical apart from the version.
3. Compare responses across versions for differences in required fields, validation strictness and error detail.
4. Check whether older versions enforce weaker validation or older authentication requirements than the current one.
5. Record every reachable version with its differences and the client that still references it, if any.
6. Feed retired versions into scope confirmation, since legacy versions frequently sit outside the documented target.

## Signals

- An older version answers with verbose stack traces or detailed validation errors the current version suppresses.
- A retired version lacks a field or check the current version enforces, hinting at weaker policy behind it.
- Versioning appears in a header or media type rather than the path, which means path-only scanners miss it entirely.
- The mobile client still calls an older base path that the web client abandoned.

## Patterns

**1. Version probe**

```text
GET /api/v1/orders/41  vs  GET /api/v2/orders/41
v1: 200, error format=verbose
diff: validation strictness, error shape, auth header name
```

**2. Version axis**

```text
path: /v1 /v2 /v3
header: X-API-Version: 1
media: application/vnd.example.v2+json
body: {"apiVersion":"2026-01-01"}
```

**3. Result row**

```text
version=v1 reachable=yes deprecated=unknown diff=verbose-errors auth=legacy-key scope=unlisted
```

## Pitfalls

- Probing versions on arbitrary hosts instead of one known operation, which multiplies requests without comparable output.
- Assuming a 404 means the version is gone when a gateway routes only specific paths to it.
- Skipping scope checks because the version prefix looks like the same application; legacy hosts are often out of scope.

## Done when

- Reachable versions are enumerated on one consistent operation with their behavioural differences recorded.
- Any version outside the documented surface is flagged for scope confirmation before deeper testing.

## References

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [OpenAPI specification - versioning](https://spec.openapis.org/oas/v3.1.0)
