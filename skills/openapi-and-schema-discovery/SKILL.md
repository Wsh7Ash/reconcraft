---
name: openapi-and-schema-discovery
description: "Find API description documents and derive the real endpoint, parameter and model surface from them. Use when the target exposes an API and you want its documented surface instead of guessing paths one request at a time"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [api, openapi, schema]
---

# OpenAPI and Schema Discovery

> Find API description documents and derive the real endpoint, parameter and model surface from them

**Use when:** the target exposes an API and you want its documented surface instead of guessing paths one request at a time

**Avoid when:** no description document exists and you are limited to passive endpoint extraction from clients

## Procedure

1. Probe conventional description locations such as swagger, openapi and api-doc paths at each known API host.
2. Validate that a response is an actual description document by checking openapi or swagger version fields and a paths object.
3. Extract every operation with its method, parameters, request models and authentication requirement.
4. Note server variables and base paths, since documents often describe staging or internal hosts alongside production.
5. Compare documented operations against endpoints you already found, which reveals undocumented routes in both directions.
6. Store a normalized operation list as a snapshot so new or removed operations show up in future diffs.

## Signals

- A document lists operations that the application never calls from its own clients, which suggests legacy or internal-only routes.
- Server entries name internal or staging hosts absent from your asset inventory.
- Schemas contain fields marked sensitive or internal, pointing at models worth inspecting during testing.
- Authentication is described as optional on operations that clearly handle account data.

## Patterns

**1. Discovery paths**

```text
/openapi.json
/swagger.json
/api/v2/api-docs
/v3/api-docs
-> validate: has "openapi" AND has "paths"
```

**2. Operation row**

```text
GET /api/v2/orders/{id} auth=bearer params=id,path required=true undocumented=no
```

**3. Coverage diff**

```text
documented 128  observed 141  undocumented=13  removed=0 -> review the 13
```

## Pitfalls

- Accepting any JSON with a paths key as the schema, which wastes time on unrelated configuration documents.
- Treating the document as complete; production APIs routinely carry routes that were never documented.
- Ignoring a stale document, since docs often lag reality and describe versions the server has retired.

## Done when

- You hold a validated operation list with methods, parameters and auth requirements, normalized for diffing.
- Undocumented and removed operations are enumerated, and any internal hosts in the document are routed to scope confirmation.

## References

- [OpenAPI specification](https://spec.openapis.org/oas/v3.1.0)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
