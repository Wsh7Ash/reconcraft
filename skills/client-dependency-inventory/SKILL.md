---
name: client-dependency-inventory
description: "Inventory the libraries, frameworks and components a browser loads, then assess each for known weakness and upgrade lag. Use when you want a defensible list of client-side components with versions to compare against published advisories"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [dependencies, components, inventory]
---

# Client Dependency Inventory

> Inventory the libraries, frameworks and components a browser loads, then assess each for known weakness and upgrade lag

**Use when:** you want a defensible list of client-side components with versions to compare against published advisories

**Avoid when:** the vendor already publishes a software bill of materials you can consume directly

## Procedure

1. Collect every script and stylesheet reference from rendered pages, including dynamically inserted and lazy-loaded assets.
2. Identify each component from file names, package metadata, banner comments and versioned paths.
3. Map identified versions to published advisory ranges, marking each component as within-range, out-of-range or unknown.
4. Separate first-party code from third-party libraries so upgrade responsibility is clear in your report.
5. Record components that are unmaintained or pinned very old, since those are maintenance risks independent of any single advisory.
6. Refresh the inventory after releases, because client bundles change without any visible application change.

## Signals

- A bundled library carries a version banner significantly behind its current release line.
- A component in your list matches a published advisory range, which is a lead to verify rather than a confirmed finding.
- Third-party scripts are loaded from URLs the vendor does not control, raising supply-chain questions.
- Same component appears at several versions across pages, indicating inconsistent bundling.

## Patterns

**1. Component row**

```text
name=library-x version=2.1.0 source=/vendor/library-x.min.js advisories=in-range(2.1.x) class=third-party
```

**2. Advisory check**

```text
version in affected range -> verify configuration before claiming impact
version outside range    -> note only
```

**3. Refresh diff**

```text
deploy 2026-10-27: library-x 2.1.0 -> 2.7.3, diff shows 4 components updated
```

## Pitfalls

- Claiming a vulnerability purely from a version match, when configuration and reachability decide actual impact.
- Listing components without source attribution, which makes the report impossible to act on.
- Re-analyzing unchanged bundles every session instead of diffing against your last inventory.

## Done when

- The inventory lists every identified component with version, source and advisory status.
- Claims are framed as hypotheses to verify, and the inventory is refreshed through diffs after each release.

## References

- [NVD - national vulnerability database](https://nvd.nist.gov/)
- [OWASP - dependency analysis guidance](https://owasp.org/)
