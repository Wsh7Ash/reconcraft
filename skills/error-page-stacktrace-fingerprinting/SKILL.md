---
name: error-page-stacktrace-fingerprinting
description: "Read application error responses for framework, component and path details that normal pages never expose. Use when an endpoint returns an error and you want to know which component produced it before you interpret the failure"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [errors, debugging, fingerprint]
---

# Error Page and Stacktrace Fingerprinting

> Read application error responses for framework, component and path details that normal pages never expose

**Use when:** an endpoint returns an error and you want to know which component produced it before you interpret the failure

**Avoid when:** the application returns uniform custom errors with no component detail, where further probing adds nothing

## Procedure

1. Trigger errors through ordinary invalid input on your own session, keeping requests rate-limited and in scope.
2. Capture full error bodies and headers rather than only status codes, since detail lives in the body.
3. Extract component names, versions, framework hints and file paths, and attribute each to the response it came from.
4. Compare errors across endpoints to learn whether one shared middleware produces them all.
5. Note whether debug detail appears only for certain content types or headers, which indicates environment leakage.
6. Record the strongest error signature as a fingerprint entry with date and evidence, then reference it in later reports.

## Signals

- A stack trace names a framework, a version and absolute paths on the server.
- Debug pages appear only when a specific content type or header is supplied, hinting at environment-dependent error handling.
- Internal hostnames or database names appear in error messages, expanding your inventory through the error path.
- Different endpoints return byte-identical error pages, meaning one shared component handles all failures.

## Patterns

**1. Error evidence**

```text
status=500 body contains: Framework 3.4.1 at /srv/app/controllers/order.py
-> component=Framework version=3.4.1 signal=path-disclosure
```

**2. Consistency check**

```text
/a -> same error hash as /b and /c  -> shared middleware
endpoint-specific errors -> local handling, worth comparing
```

**3. Signature record**

```text
host=api.example.com error_class=framework-debug evidence=version+path date=2026-10-27 severity=informational
```

## Pitfalls

- Reproducing an error many times in a burst, which looks like an availability test rather than a single probe.
- Quoting absolute server paths in a public report without considering whether they reveal sensitive deployment detail.
- Assuming a version string in an error is authoritative when deployments frequently patch without bumping it.

## Done when

- Each error signature is attributed to a component with evidence, and cross-endpoint consistency is documented.
- Findings are recorded with dates and severity context rather than raw output dumped into notes.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [CWE - information exposure through error messages](https://cwe.mitre.org/)
