---
name: object-id-surface-mapping
description: "Map where the application exposes object identifiers, which is the first step toward reviewing object-level authorization. Use when the application is API-driven or parameterized by identifiers, and you need a list of every identifier entry point"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [idor, api, authorization]
---

# Object ID Surface Mapping

> Map where the application exposes object identifiers, which is the first step toward reviewing object-level authorization

**Use when:** the application is API-driven or parameterized by identifiers, and you need a list of every identifier entry point

**Avoid when:** the interface exposes no identifiers at all, where the surface simply does not exist to map

## Procedure

1. Collect identifier-bearing locations from responses: paths, query strings, request bodies, headers and pagination tokens.
2. Classify each identifier: sequential integer, UUID, composite key, opaque token or encoded structure.
3. Note which identifiers appear in responses the client is not meant to edit, since those are the classic exposure points.
4. Trace where each identifier flows: read operation, write operation, export or deletion path.
5. Group identifiers by object type so later review can reason per resource rather than per request.
6. Store the map as a table linking identifier, location, operation and object type for the next testing phase.

## Signals

- Sequential integers appear in paths for objects that clearly belong to different accounts.
- Identifiers leak into responses for objects the current session has no legitimate relationship with.
- Encoded structures decode into predictable fields such as account id and role.
- Pagination tokens embed the previous query's identifiers, revealing objects beyond the current view.

## Patterns

**1. Identifier table**

```text
location=/orders/{id} type=int      op=read  object=order  flow=response->request
location=X-Object-Id  type=uuid    op=write object=file   flow=response->header
```

**2. Classification**

```text
sequential -> predictability risk, prioritize review
uuid       -> not predictable, still needs authorization check
encoded    -> decode offline, fields often include role or owner
```

**3. Scope note**

```text
map only; do not walk other users' objects without authorization to test with your own data
```

## Pitfalls

- Treating identifier mapping as proof of a vulnerability, when the actual check happens server-side and untested.
- Accessing objects that belong to other users during mapping, which crosses an authorization boundary you have not been granted.
- Mapping only paths and missing identifiers that hide in headers, bodies and tokens.

## Done when

- Every identifier location is recorded with type, operation and object type, drawn from all four positions.
- Mapping used only your own data and objects, and the resulting table is queued for authorized access-control review.

## References

- [OWASP API Security Top 10 - BOLA](https://owasp.org/www-project-api-security/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
