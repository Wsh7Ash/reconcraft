---
name: duplicate-hypothesis-checking
description: "Before writing a report, check whether your finding is already known, already fixed, or already reported by someone else. Use when you have a plausible finding and are about to spend time writing it up for submission"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [triage, duplicates, reporting]
---

# Duplicate Hypothesis Checking

> Before writing a report, check whether your finding is already known, already fixed, or already reported by someone else

**Use when:** you have a plausible finding and are about to spend time writing it up for submission

**Avoid when:** the issue is clearly novel and time-critical, where you should report first and refine after

## Procedure

1. Search the program's disclosed reports and your own earlier notes for the same root cause, not just the same symptom.
2. Check whether the behaviour still reproduces after your last test, since fixes often land silently between sessions.
3. Compare your root cause against known advisories to see whether this is a known component issue rather than a novel one.
4. Check whether your report would be a duplicate of another researcher's in-flight work under the program's rules.
5. Decide: report as new, report as additional impact on an existing issue, or close as duplicate, and record why.
6. Keep the evidence that supports your novelty claim, because triage will ask for exactly that.

## Signals

- A disclosed report from last year describes the same root cause on a different endpoint.
- The behaviour stops reproducing, which usually means a fix landed and your report is stale.
- Your finding is one instance of a pattern affecting many routes, which changes it from a bug to a systemic note.
- The program's FAQ says duplicates within a certain window are treated as informational.

## Patterns

**1. Novelty check**

```text
same root cause found in disclosed report #1234 -> duplicate
same root cause, broader impact here -> additional-impact report
```

**2. Re-verify**

```text
reproduce 3x today after fix-cadence check -> still present, report now
```

**3. Decision record**

```text
finding=stale-cache-key decision=new reason=no-disclosed-match reverified=2026-10-27
```

## Pitfalls

- Checking only titles or symptoms, when two superficially different symptoms often share one root cause.
- Skipping re-verification and reporting an issue the vendor already resolved.
- Assuming novelty without searching disclosed reports, which is the fastest way to waste triage time.

## Done when

- You searched disclosed reports and your own notes for the root cause and re-verified reproduction today.
- The decision (new, additional, duplicate) is recorded with the evidence that supports it.

## References

- [HackerOne - duplicate handling and triage](https://hackerone.com/blog)
- [Bugcrowd - researcher resources](https://www.bugcrowd.com/blog/)
