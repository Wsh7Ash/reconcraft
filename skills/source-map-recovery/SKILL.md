---
name: source-map-recovery
description: "Locate and read published source maps and build artifacts to recover original file structure, comments and build configuration. Use when a JavaScript bundle ships a sourceMappingURL comment or the build exposes map files alongside assets"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [javascript, source-maps, build]
---

# Source Map Recovery

> Locate and read published source maps and build artifacts to recover original file structure, comments and build configuration

**Use when:** a JavaScript bundle ships a sourceMappingURL comment or the build exposes map files alongside assets

**Avoid when:** no map files exist and decompiling minified code would cost far more time than the application surface justifies

## Procedure

1. Check each downloaded bundle for a sourceMappingURL comment at its end and for sibling .map files at predictable paths.
2. Fetch candidate maps and confirm they are genuine maps with valid sources arrays rather than unrelated error pages.
3. Read the sourcesContent arrays to recover original file paths, developer comments and internal module names.
4. Extract file paths, directory conventions and build tooling hints that reveal how the application is organized.
5. Map recovered symbols back to endpoints and configuration so the discovery feeds later phases rather than sitting in a folder.
6. Record which bundle exposed each map, then re-check after a release because production builds change frequently.

## Signals

- A bundle ends with a sourceMappingURL pointing at a file served from the same origin.
- Recovered sources contain internal paths such as src/features/admin that never appear in public navigation.
- Original files include commented-out endpoints, feature flags or environment variables.
- Maps reference a separate build host or repository name that expands your asset inventory.

## Patterns

**1. Map lookup**

```text
GET /assets/main.77ab.js   tail: //# sourceMappingURL=main.77ab.js.map
GET /assets/main.77ab.js.map  -> {"version":3,"sources":["../src/app.ts"],...}
```

**2. Recovery value**

```text
sources: src/api/client.ts, src/admin/routes.ts, src/config/env.ts
comment in client.ts: // staging host: api.staging.example.com
```

**3. Result row**

```text
bundle=main.77ab.js map=found sources=41 internal_paths=12 class=recoverable
```

## Pitfalls

- Saving maps without verifying structure, so an HTML error page served with a 200 status is mistaken for a source map.
- Publishing recovered internal file paths in a report without checking they are not customer-confident identifiers.
- Ignoring that maps rotate per build, which makes old recovery results stale after the next deploy.

## Done when

- Each recovered map is validated as real JSON with a sources array and is attributed to its bundle.
- Extracted internal paths, flags and endpoints are transferred into your inventory and endpoint list, not left in a downloads folder.

## References

- [Source map specification](https://tc39.es/source-map/)
- [MDN - HTML source mapping](https://developer.mozilla.org/en-US/docs/Web/API/SourceMap)
