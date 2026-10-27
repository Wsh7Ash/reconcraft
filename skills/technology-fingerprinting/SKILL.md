---
name: technology-fingerprinting
description: "Identify the frameworks, servers and services behind a host from many weak signals so you know which behaviour to expect. Use when you need to know what software stack you are facing before designing tests or interpreting an error"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [fingerprint, stack, headers]
---

# Technology Fingerprinting

> Identify the frameworks, servers and services behind a host from many weak signals so you know which behaviour to expect

**Use when:** you need to know what software stack you are facing before designing tests or interpreting an error

**Avoid when:** the vendor publishes its architecture documentation and your first request already matches it

## Procedure

1. Collect response headers, cookies, HTML markers, script paths and TLS certificate details from a single consistent request set.
2. Match each signal against known technology signatures, keeping the evidence next to every identification.
3. Weigh signals by reliability: framework runtime cookies and generator tags beat generic server headers.
4. Note contradictions, such as a server header naming one product while assets clearly come from another.
5. Record version claims separately from product claims, since versions often lag or are deliberately hidden.
6. Store the fingerprint with date and evidence so changes after a migration become visible in later runs.

## Signals

- Cookies carry framework names with session identifiers, which is a stronger signal than a generic server header.
- Asset URLs follow a framework's built-in convention such as static asset folders or asset hash naming.
- A generator meta tag names a content platform and version.
- Headers contradict each other, meaning a proxy or front layer is rewriting what the origin would send.

## Patterns

**1. Evidence row**

```text
signal=Set-Cookie: PHPSESSID evidence=header weight=high -> PHP
signal=/static/js/main.8f21.css evidence=path weight=medium -> bundler pipeline
```

**2. Confidence**

```text
high: framework runtime cookie, generator tag, known default path
medium: header, asset convention
low: server header alone (often spoofed)
```

**3. Snapshot**

```text
host=app.example.com stack=nginx,php,react captured=2026-10-27 confidence=medium
```

## Pitfalls

- Believing the server header, which is one of the most commonly altered fields in production responses.
- Confusing the CDN's technology with the origin application's technology.
- Recording a fingerprint without evidence, making later results impossible to challenge or update.

## Done when

- Each identified technology carries at least one concrete evidence string and a confidence level.
- The fingerprint is stored with its capture date, and contradictions between signals are noted rather than smoothed over.

## References

- [Wappalyzer - detection concepts](https://www.wappalyzer.com/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
