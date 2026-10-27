---
name: canonical-host-and-aliasing-checks
description: "Establish which hostname is canonical for each application and which aliases reach it, so your results stay attributable. Use when several hostnames answer with the same application, or you are unsure which name your results should be filed against"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [canonical, hostnames, aliasing]
---

# Canonical Host and Aliasing Checks

> Establish which hostname is canonical for each application and which aliases reach it, so your results stay attributable

**Use when:** several hostnames answer with the same application, or you are unsure which name your results should be filed against

**Avoid when:** the program documents one canonical host per application and your inventory already matches it

## Procedure

1. Request each alias with and without the canonical host header and compare bodies, status and redirect targets.
2. Record how the application decides canonical behaviour: host header, redirect, cookie or absolute links inside pages.
3. Check whether cookies are scoped to one hostname or shared across aliases, which affects session handling later.
4. Confirm that content is genuinely identical by hashing bodies rather than eyeballing titles.
5. Document which aliases are marketing redirects, which are functional and which serve a different application.
6. Update inventory so each application has one canonical entry with its aliases attached.

## Signals

- Two hostnames serve byte-identical content, meaning later tests against both are duplicates.
- A cookie set on one alias is sent to another, which is a session-sharing question worth documenting.
- One alias serves an older build of the same application, hinting at a deployment lag.
- Absolute links inside a page point at a different hostname than the one you requested.

## Patterns

**1. Alias table**

```text
www.example.com   -> 301 -> https://example.com  (redirect alias)
app.example.com   -> 200, hash=11bc  canonical
old.example.com   -> 200, hash=77de  stale build
```

**2. Host test**

```text
Host: app.example.com  vs Host: unknown.example.com
identical body -> default vhost, canonical decision lives elsewhere
```

**3. Canonical record**

```text
app=example.com canonical=yes aliases=[www, portal] cookie_scope=exact-host
```

## Pitfalls

- Filing the same finding twice under two aliases, which wastes triage time and damages credibility.
- Assuming identical titles mean identical content, when body hashes frequently differ behind the same title.
- Overlooking a stale alias running old code, which is often the least-patched copy of the application.

## Done when

- Each application has one canonical hostname with alias relationships and cookie scoping recorded.
- Duplicate-content aliases are marked so future findings are filed once, against the canonical entry.

## References

- [RFC 9110 - target reference and host semantics](https://www.rfc-editor.org/rfc/rfc9110)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
