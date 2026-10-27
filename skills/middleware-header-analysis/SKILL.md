---
name: middleware-header-analysis
description: "Read response headers as a map of the middleware chain in front of the application, from cache layers to security controls. Use when you want to know which intermediate layers process a request before the application itself does"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [headers, middleware, http]
---

# Middleware Header Analysis

> Read response headers as a map of the middleware chain in front of the application, from cache layers to security controls

**Use when:** you want to know which intermediate layers process a request before the application itself does

**Avoid when:** a single response already shows a trivial stack and you have no reason to compare multiple paths

## Procedure

1. Capture full response headers from several representative paths: static asset, dynamic page and API endpoint.
2. Order the observed layers from edge inward: proxy, cache, application server, framework, application.
3. Note security control headers such as content security policy, frame protection, referrer policy and permissions policy.
4. Identify cache participation from age, cache-control, vary and any edge-specific cache headers.
5. Look for headers that leak internal details such as internal request ids, backend names or trace identifiers.
6. Record the header profile per path type so later changes after a configuration update show up as diffs.

## Signals

- Age and cache headers appear on dynamic pages, meaning responses may be shared between users.
- Internal-sounding request identifiers or backend names appear in headers sent to every client.
- Security headers exist on one path but are missing on another, indicating inconsistent middleware application.
- The vary header changes between paths, showing where content negotiation and caching split.

## Patterns

**1. Header profile**

```text
static:  cache-control=public,max-age=31536000, age=4211
dynamic: cache-control=no-store, vary=Cookie, set-cookie=...; HttpOnly
```

**2. Layer order**

```text
edge proxy -> cache -> app server -> framework -> handler
evidence: server header, age, x-request-id, framework cookie
```

**3. Control checklist**

```text
content-security-policy, x-frame-options or frame-ancestors,
referrer-policy, permissions-policy, cross-origin policies
```

## Pitfalls

- Reading headers from one path and generalizing to the whole application, where middleware often differs by route.
- Ignoring the vary header, which changes whether a cached response can leak between users.
- Treating the presence of a security header as proof it is correctly configured; directives matter more than existence.

## Done when

- You have a per-path header profile with the middleware order and cache participation recorded.
- Missing or inconsistent security controls are listed per path type with the evidence captured.

## References

- [RFC 9111 - HTTP caching](https://www.rfc-editor.org/rfc/rfc9111)
- [securityheaders.com reference](https://securityheaders.com/)
