---
name: attack-surface-change-review
description: "Diff two recon snapshots and turn the differences into a short, prioritized list of what to test next. Use when you have two snapshots from different dates, or a vendor announces a change you need to evaluate"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [diff, priorities, snapshots]
---

# Attack Surface Change Review

> Diff two recon snapshots and turn the differences into a short, prioritized list of what to test next

**Use when:** you have two snapshots from different dates, or a vendor announces a change you need to evaluate

**Avoid when:** nothing has changed since your last run and you only need confirmation rather than a work list

## Procedure

1. Load both snapshots and normalize identifiers so the diff compares entities rather than raw text lines.
2. Classify every change: added asset, removed asset, changed configuration and changed ownership or scope.
3. Rank additions by exposure: internet-reachable new hosts and newly public storage outrank internal naming changes.
4. Check whether any change moved an asset in or out of program scope, which alters what you may test.
5. Produce a short work list of the top changes with the evidence line for each, rather than a raw diff dump.
6. Store the review as the bridge between recon and the next testing session.

## Signals

- A new host appears that resolves publicly and is absent from the program's published asset list.
- An asset moves out of scope, which means existing test plans must be re-checked before continuing.
- A previously private endpoint becomes publicly reachable after a redeployment.
- Configuration changed on a host you already tested, invalidating parts of your earlier conclusions.

## Patterns

**1. Diff classes**

```text
+added host app2.example.com reachable=yes scope=unlisted -> ask, then prioritize
-removed host old.example.com -> close open questions
~changed header profile on app.example.com -> re-test controls
```

**2. Change ranking**

```text
1 new public host  2 newly public storage  3 config change  4 naming-only
```

**3. Work list**

```text
item=1 action=scope-confirm+test evidence=added host resolves 2026-10-27
```

## Pitfalls

- Publishing a raw diff instead of a ranked list, which forces the reviewer to do your prioritization.
- Testing a newly added asset before confirming scope, even though additions are exactly where scope changes fastest.
- Ignoring removals, which often mark decommissioned systems that may still answer somewhere.

## Done when

- The review lists ranked changes with evidence and scope status, ready to become a test plan.
- Any asset that left scope is flagged, and pending work against it is paused until confirmed.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackTricks - recon methodology](https://book.hacktricks.xyz/)
