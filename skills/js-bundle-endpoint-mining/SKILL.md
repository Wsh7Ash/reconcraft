---
name: js-bundle-endpoint-mining
description: "Pull API routes, hidden parameters and environment values out of the application's own JavaScript bundles. Use when you face a modern single-page application whose HTML reveals almost no surface but whose scripts reference the real backend"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [javascript, endpoints, discovery]
---

# JavaScript Bundle Endpoint Mining

> Pull API routes, hidden parameters and environment values out of the application's own JavaScript bundles

**Use when:** you face a modern single-page application whose HTML reveals almost no surface but whose scripts reference the real backend

**Avoid when:** the site serves plain server-rendered pages with no bundled scripts, where crawling already exposes the routes

## Procedure

1. Collect every script reference from the HTML, including dynamically injected module preload links and inline source hints.
2. Download the bundles and record which file each endpoint came from, so findings stay attributable during triage.
3. Extract candidate routes with patterns for relative paths, absolute API bases and template-built URLs.
4. Pull out parameter names, header names and environment configuration such as feature flags and API versions.
5. Deduplicate and normalize endpoints, resolving relative paths against the script's own location rather than the page URL.
6. Queue the unique endpoints for schema discovery, keeping any that reference internal hostnames or non-public domains flagged separately.

## Signals

- A bundle hardcodes an API base URL on a different subdomain that never appears in the crawled HTML.
- Feature flags or environment objects reveal toggles such as beta or internal that change application behaviour.
- Source contains parameter names absent from the user interface, which usually means undiscovered request surface.
- Comments or build metadata name internal tooling, versions or repository paths.

## Patterns

**1. Extraction patterns**

```text
url("/api/v2/orders")
base: "https://api.internal.example.com"
headers: { "X-Request-Source": "web" }
params: ['accountId', 'debug', 'includeArchived']
```

**2. Normalization**

```text
script=https://app.example.com/main.77ab.js
relative /api/orders -> https://app.example.com/api/orders
absolute kept as-is, host recorded separately
```

**3. Result row**

```text
endpoint=/api/v2/orders method=GET source=main.77ab.js params=accountId,includeArchived
```

## Pitfalls

- Extracting endpoints without recording the source file, which makes later triage unable to justify why a path matters.
- Treating minified variable names as parameters, flooding your list with build artifacts instead of request surface.
- Forgetting to re-run after a deploy, since bundles change on every release and stale extraction hides new endpoints.

## Done when

- Every extracted endpoint is normalized, attributed to a source file and deduplicated against your crawl results.
- Endpoints on non-public hosts are separated and marked for scope confirmation before any request is sent to them.

## References

- [PortSwigger - working with JavaScript](https://portswigger.net/web-security)
- [MDN - JavaScript modules](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules)
