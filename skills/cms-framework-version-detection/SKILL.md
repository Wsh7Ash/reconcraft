---
name: cms-framework-version-detection
description: "Pin down a content platform's exact version from public artifacts to compare against known advisories you are authorized to assess. Use when a content platform or framework is identified and version-specific advisories could explain observed behaviour"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [version, cms, advisories]
---

# CMS and Framework Version Detection

> Pin down a content platform's exact version from public artifacts to compare against known advisories you are authorized to assess

**Use when:** a content platform or framework is identified and version-specific advisories could explain observed behaviour

**Avoid when:** the product has no observable version markers and version hunting would consume the whole testing window

## Procedure

1. Look for explicit version markers in meta tags, generator tags, feed URLs, asset query strings and changelog endpoints.
2. Compare asset file naming conventions and built-in paths against known versions of the identified product.
3. Check release and manifest endpoints the product ships by default, which often state a version plainly.
4. Cross-check your candidate version against at least two independent signals before treating it as fact.
5. Map the confirmed version to published advisories and record which ones are relevant, without assuming applicability.
6. Store the version with evidence and the date, since platforms upgrade silently and old conclusions expire.

## Signals

- A generator tag states a full product and version string directly in the page head.
- Asset query strings embed a version that differs from the generator tag, suggesting a partial upgrade.
- A manifest or changelog endpoint returns a version the front-end does not advertise.
- The identified version matches an end-of-life release line, which is worth reporting as a maintenance risk.

## Patterns

**1. Version evidence**

```text
generator meta = Product 4.7.2
asset path     = /assets/v4.7.2/main.css
manifest       = {"version":"4.7.2"}   agree -> confirmed
```

**2. Advisory mapping**

```text
version=4.7.2 line=4.7 advisories=[CVE-....-A, CVE-....-B]
relevance=verify-configuration, do not assume vulnerable
```

**3. Version record**

```text
host=www.example.com product=Product version=4.7.2 evidence=3-signal-agreement date=2026-10-27
```

## Pitfalls

- Declaring a version from one marker, which is frequently wrong behind a proxy or a customized build.
- Assuming an advisory applies because the version range matches; configuration and backports change applicability.
- Skipping the re-check after a vendor patch, leaving your report citing an outdated version.

## Done when

- The version is confirmed by at least two independent signals, each recorded with its evidence.
- Relevant advisories are listed as hypotheses to verify against observed behaviour, not as confirmed vulnerabilities.

## References

- [NVD - national vulnerability database](https://nvd.nist.gov/)
- [CWE - common weakness enumeration](https://cwe.mitre.org/)
