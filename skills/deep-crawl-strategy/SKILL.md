---
name: deep-crawl-strategy
description: "Crawl a modern application exhaustively with a frontier you control, so dynamic rendering and infinite loops do not decide your coverage. Use when the application is a single-page app or a large multi-page site where a naive crawler either stops early or loops forever"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [crawling, coverage, frontier]
---

# Deep Crawl Strategy

> Crawl a modern application exhaustively with a frontier you control, so dynamic rendering and infinite loops do not decide your coverage

**Use when:** the application is a single-page app or a large multi-page site where a naive crawler either stops early or loops forever

**Avoid when:** you are reviewing a small fixed set of known URLs where a scripted fetch list is faster than a crawler

## Procedure

1. Seed the frontier from every source you have: crawl results, sitemaps, extracted script endpoints and archived links.
2. Set explicit bounds: maximum depth, maximum pages and a domain allow list that prevents escape into third-party sites.
3. Render pages before extracting links, since client-side routers only emit their links after scripts run.
4. Deduplicate on normalized URLs so query ordering and session tokens cannot spawn infinite frontier growth.
5. Record for each visited URL its source link, status, type and whether it required authentication.
6. Export the visited set as a snapshot that future crawls diff, which shows new pages the application actually added.

## Signals

- The frontier grows without bound because session IDs or cache-busting parameters create unique URLs forever.
- Pages only appear after rendering, meaning a static fetch pass reports far less surface than exists.
- Crawl output includes external hosts, showing your allow list is not enforced at the connection layer.
- A cluster of URLs shares one template with only identifiers changing, which should collapse into one route pattern.

## Patterns

**1. Normalization**

```text
https://app/x?id=1&ref=nav   + https://app/x?ref=nav&id=1  -> same key
strip: session params, sort query, resolve ./ and ../, drop fragment
```

**2. Crawl bounds**

```text
max_depth=6, max_pages=5000, host_allow=[app.example.com], external=no
```

**3. Snapshot row**

```text
url | route_pattern | status | auth | source_link
/orders/4821 -> /orders/{id} | 200 | yes | /orders
```

## Pitfalls

- Letting the crawler follow every link including third-party widgets, which wastes budget and sends traffic off scope.
- Skipping normalization so parameterized URLs multiply until the crawl never finishes.
- Treating page count as coverage; unique route patterns are the metric that matters for later testing.

## Done when

- The crawl terminates within its bounds and yields a deduplicated set of route patterns with auth flags.
- The visited set is stored as a diffable snapshot, and external hosts were excluded by an enforced allow list.

## References

- [PortSwigger - content discovery](https://portswigger.net/web-security/content-discovery)
- [MDN - client-side routing concepts](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
