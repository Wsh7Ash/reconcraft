---
name: cdn-waf-origin-attribution
description: "Work out whether you are talking to an edge or to the origin, without probing infrastructure that is not yours. Use when a host sits behind a content delivery network and you need to know what your requests are actually reaching"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [cdn, origin, infrastructure]
---

# CDN and WAF Origin Attribution

> Work out whether you are talking to an edge or to the origin, without probing infrastructure that is not yours

**Use when:** a host sits behind a content delivery network and you need to know what your requests are actually reaching

**Avoid when:** the application is served directly from vendor infrastructure with no intermediary visible in responses

## Procedure

1. Identify the edge provider from headers, certificate details and address ranges, all of which come from public data.
2. Compare responses across hostnames sharing one edge to see which differences come from the edge rather than the app.
3. Check whether custom hostnames or direct-to-origin routes exist in your inventory, since those bypass the edge entirely.
4. Use only passive or in-scope signals to infer origin candidates; do not scan third-party address space hunting for one.
5. Record the verdict per hostname: edge-served, edge-with-known-origin, or direct, with the evidence you used.
6. Treat origin hostnames found in public records as separate scope questions before any request goes to them.

## Signals

- Edge cache headers and provider-specific response headers appear on every path.
- Two hostnames on the same edge return different application behaviour, showing the edge is not what differs.
- A certificate or DNS record names an origin hostname, which becomes a scope question rather than an automatic target.
- Direct requests with a provider host header return a different error page than normal application errors.

## Patterns

**1. Edge evidence**

```text
headers: cf-ray, x-cache: HIT, via: 1.1 provider
addresses: provider edge range
verdict: edge-served
```

**2. Origin notes**

```text
origin candidate found in public dns -> class=unlisted -> ask program first
no origin found -> proceed with hostname-only testing
```

**3. Attribution record**

```text
host=www.example.com edge=provider verdict=edge-served origin=none method=passive
```

## Pitfalls

- Port-scanning provider ranges looking for the origin, which is out of scope by definition and often prohibited.
- Assuming the edge enforces the origin's security policy, when the origin may accept direct requests the edge blocks.
- Reporting an edge cache behaviour as an application bug without proving where the response was produced.

## Done when

- Each hostname has an edge or direct verdict backed by recorded evidence, and origin candidates are scope questions.
- No traffic you generated was aimed at infrastructure outside the program's declared assets.

## References

- [RFC 9111 - HTTP caching](https://www.rfc-editor.org/rfc/rfc9111)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
