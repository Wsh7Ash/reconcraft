---
name: mobile-backend-endpoint-extraction
description: "Recover API hosts, headers and feature flags from a mobile application package you are authorized to analyze. Use when a program ships Android or iOS clients whose backends are not reachable from the web application"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [mobile, api, static-analysis]
---

# Mobile Backend Endpoint Extraction

> Recover API hosts, headers and feature flags from a mobile application package you are authorized to analyze

**Use when:** a program ships Android or iOS clients whose backends are not reachable from the web application

**Avoid when:** the vendor supplies an API description directly, which already gives you the same surface faster

## Procedure

1. Obtain the application package through official channels for a version you are allowed to test, and record the version you used.
2. Extract strings, embedded configuration and resource files, searching for absolute URLs, base paths and environment switches.
3. Identify hardcoded keys and headers, classifying each as public client identifier or secret-looking material to report carefully.
4. Trace feature flags and environment endpoints such as staging or debug hosts that may lead to less-protected systems.
5. Normalize the recovered endpoints into your inventory with the package version as their source attribution.
6. Re-run the extraction after application updates, since clients routinely ship new hosts in each release.

## Signals

- The package contains base URLs for staging or debug environments alongside production.
- Embedded configuration references internal hostnames that never appear in public DNS data.
- A hardcoded key is labeled with a name suggesting administrative or service-level privilege.
- Feature flags expose toggles that alter authentication or validation behaviour on the backend.

## Patterns

**1. Extraction set**

```text
https://api.example.com/v3
https://staging.api.example.com
header: X-Client-Id: <value>
flag: enable_legacy_auth=true
```

**2. Classification**

```text
public client id -> note only
secret-shaped     -> report for rotation, never publish the value
```

**3. Attribution**

```text
endpoint=https://staging.api.example.com source=app-v4.2.0 package=arm64 captured=2026-10-27
```

## Pitfalls

- Publishing extracted key material in a report, which converts a finding into an active leak.
- Testing a staging host before confirming it is inside program scope, since staging is often explicitly excluded.
- Analyzing only the newest package, missing hosts that older clients still call and servers still accept.

## Done when

- Recovered endpoints and flags are normalized into inventory with package version attribution.
- Secret-shaped values are described but never reproduced, and any non-production host is scope-checked before use.

## References

- [OWASP MASVS - mobile application security](https://owasp.org/www-project-mobile-app-security/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
