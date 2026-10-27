---
name: waf-presence-detection
description: "Determine whether a web application firewall is filtering your traffic, and what that means for coverage and false results. Use when requests return generic block pages, unusual 403 or 406 responses, or your scanner results suddenly look inconsistent"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [waf, filtering, http]
---

# WAF Presence Detection

> Determine whether a web application firewall is filtering your traffic, and what that means for coverage and false results

**Use when:** requests return generic block pages, unusual 403 or 406 responses, or your scanner results suddenly look inconsistent

**Avoid when:** responses are uniform and transparent, with no blocking behaviour anywhere in your test set

## Procedure

1. Send a small set of obviously synthetic markers and observe whether a generic block page or challenge replaces the application response.
2. Compare blocked responses across paths to learn whether filtering is global or applies only to certain routes.
3. Check whether static assets pass while dynamic requests are filtered, which localizes the control to the request path.
4. Note challenge types such as JavaScript challenges or interstitial pages, since they change how automated tools should behave.
5. Record which classes of input trigger filtering, which informs how you phrase tests rather than how you bypass them.
6. Treat a filter that blocks your test class as a coverage boundary to document, not an obstacle to defeat on a target you do not own.

## Signals

- A synthetic marker returns a branded block page with a request identifier and no application content.
- Static assets answer normally while query strings containing marker text are refused.
- Responses switch from 200 to 403 or 406 only when specific characters appear in input.
- A challenge page appears for one client profile but not for a plain browser-like request.

## Patterns

**1. Marker test**

```text
GET /search?q=<marker-test-string>
baseline: 200 len=12033
with marker: 403 len=742 block-page=yes -> filtering present
```

**2. Path split**

```text
static /assets/*  -> 200 for all markers
dynamic /search    -> 403 for markers
verdict: filtering on dynamic path only
```

**3. Filter record**

```text
host=www.example.com filter=present scope=global evidence=block-page-with-request-id date=2026-10-27
```

## Pitfalls

- Interpreting a block page as an application error, which sends your triage in the wrong direction entirely.
- Running aggressive payloads repeatedly against the filter, which violates rate rules and gains nothing on an authorized target.
- Concluding coverage that a filter silently prevented, so your results understate what the application would otherwise reveal.

## Done when

- Filter presence, scope and trigger classes are recorded with the block-page evidence attached.
- Coverage limitations caused by filtering are documented, and no attempt was made to defeat protections on the vendor's systems.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [PortSwigger - web cache and edge behaviour](https://portswigger.net/web-security)
