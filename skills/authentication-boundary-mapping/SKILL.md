---
name: authentication-boundary-mapping
description: "Chart which routes, methods and operations require which credential, so public and protected surfaces are unambiguous. Use when you need a clear picture of where authentication starts and stops before you review session or access-control behaviour"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [authentication, boundaries, mapping]
---

# Authentication Boundary Mapping

> Chart which routes, methods and operations require which credential, so public and protected surfaces are unambiguous

**Use when:** you need a clear picture of where authentication starts and stops before you review session or access-control behaviour

**Avoid when:** a single unauthenticated route exists and your target is that one path alone

## Procedure

1. Enumerate representative routes per area of the application, including at least one per method and resource type.
2. Request each route unauthenticated with session material fully removed, and record status and response shape.
3. Repeat with your authorized account to see exactly what the credential changes in the response.
4. Check whether authentication is enforced at the edge, at the framework or inside handlers, based on error consistency.
5. Look for routes that differ only by method, since a protected GET with a public POST is a classic boundary gap.
6. Produce a route-by-route boundary table and hand it to the authorization review phase.

## Signals

- A route returns full data unauthenticated while its sibling requires a session.
- Error shape differs between edge rejection and application rejection, revealing where the check happens.
- Some methods on a path are protected while others pass through unauthenticated.
- A redirect to login on one route but a plain 401 on another indicates inconsistent boundary enforcement.

## Patterns

**1. Boundary table**

```text
route            | GET unauth | GET auth | POST unauth
/api/me          | 401        | 200      | 401
/api/public/feed | 200        | 200      | 403
/export.csv      | 200        | 200      | 200  <- review
```

**2. Rejection origin**

```text
edge: generic 401 + provider headers
framework: structured error with code
handler: application-specific body
```

**3. Method split record**

```text
method-level split: path=/api/items GET=auth-required POST=public -> flag for review
```

## Pitfalls

- Testing boundaries while still holding a session cookie, which silently authenticates requests you believe are anonymous.
- Recording only status codes and missing cases where the response body differs while status stays 200.
- Assuming edge enforcement applies to every backend route, when internal services often rely on the edge entirely.

## Done when

- A route-by-method table shows unauthenticated and authenticated behaviour for every sampled area.
- Boundary inconsistencies are flagged with exact evidence, and all requests used your own credentials or none at all.

## References

- [OWASP API Security Top 10 - broken authentication](https://owasp.org/www-project-api-security/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
