---
name: status-code-response-size-baselining
description: "Learn what each status code and response size means in this application so scanner output can be triaged instead of trusted. Use when a scan produces hundreds of results and you need reliable rules for separating signal from application-specific noise"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [status-codes, triage, baseline]
---

# Status Code and Response Size Baselining

> Learn what each status code and response size means in this application so scanner output can be triaged instead of trusted

**Use when:** a scan produces hundreds of results and you need reliable rules for separating signal from application-specific noise

**Avoid when:** you are reviewing a single endpoint by hand where a full classification scheme is unnecessary overhead

## Procedure

1. Request a known-existing path, a known-missing path and a forbidden path to learn this application's three reference responses.
2. Measure the size distribution of each reference class, since many applications return the same error body for every miss.
3. Identify soft-404 behaviour where a missing resource still answers with status 200.
4. Check whether authentication changes status codes, since an unauthenticated request may turn 404 into 401 or 403.
5. Write the classification rules into a small profile your later scans can apply automatically.
6. Re-verify the profile when the application changes its error pages or error handling middleware.

## Signals

- Missing paths return 200 with a body identical to every other missing path, marking a classic soft-404.
- The same path returns 404 unauthenticated and 200 authenticated, meaning status depends on session state.
- Error bodies share a fixed length across thousands of paths, which makes length a reliable classifier here.
- A CDN returns its own 404 page while the origin would return the application's, so edge and origin differ.

## Patterns

**1. Reference set**

```text
exists   -> 200 len=48210 type=text/html
missing  -> 200 len=9821  type=text/html hash=aa41 (soft-404)
forbidden-> 403 len=742   type=text/html
```

**2. Classifier**

```text
len==9821 AND hash==aa41 -> MISSING
len==742 -> FORBIDDEN
otherwise -> interesting, queue for review
```

**3. Auth variant**

```text
unauth GET /admin -> 401   auth GET /admin -> 200 (role-gated, not missing)
```

## Pitfalls

- Trusting 404 as missing on an application that returns 200 for everything, which inverts your entire triage.
- Mixing authenticated and unauthenticated results in one profile and then wondering why statuses contradict.
- Ignoring compression, which changes size enough to invalidate thresholds you measured earlier.

## Done when

- Reference responses exist for exists, missing and forbidden, each with size and hash characteristics recorded.
- A classification rule set is written down and validated against a fresh sample of known paths.

## References

- [RFC 9110 - response status codes](https://www.rfc-editor.org/rfc/rfc9110)
- [PortSwigger - content discovery](https://portswigger.net/web-security/content-discovery)
