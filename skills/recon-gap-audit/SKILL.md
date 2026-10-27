---
name: recon-gap-audit
description: "Audit your own recon for what is missing, biased or unverified, before you claim coverage to anyone else. Use when you are about to declare recon complete, or a test session produced surprisingly few leads"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [coverage, audit, quality]
---

# Recon Gap Audit

> Audit your own recon for what is missing, biased or unverified, before you claim coverage to anyone else

**Use when:** you are about to declare recon complete, or a test session produced surprisingly few leads

**Avoid when:** recon is still in its first exploratory pass where gaps are expected by definition

## Procedure

1. List every asset class the program could plausibly expose and mark which ones your recon actually touched.
2. Review each dataset for bias: one resolver, one wordlist or one certificate source gives one partial view.
3. Find records you collected but never followed up, since forgotten leads are the most common silent gap.
4. Check whether scope uncertainty suppressed work: unlisted items parked without an answer stall entire areas.
5. Rank the gaps by likely impact and state the cheapest way to close each one.
6. Write the audit as a short document that says plainly what you do not know yet.

## Signals

- An asset class such as mobile backend or mail infrastructure has no entries at all in your inventory.
- Every host in your list came from a single source, which means one dataset change would rewrite your view.
- Items marked unlisted have been sitting untouched for weeks with no question sent to the program.
- Your endpoint list grew from crawling only, with no schema or script-derived endpoints merged in.

## Patterns

**1. Gap table**

```text
class=mobile-backend touched=no cost=medium impact=high -> extract from package
class=mail touched=yes  cost=low    impact=low  -> fine
```

**2. Bias check**

```text
sources per host: dns=1 only for 38/214 hosts -> add certificate or archive source
```

**3. Audit line**

```text
gap=unlisted-parked count=12 oldest=2026-09-30 action=send-scope-question
```

## Pitfalls

- Declaring coverage based on volume, when 10,000 endpoints from one crawler can still miss an entire asset class.
- Auditing only what you measured, so missing datasets never appear in the gap list at all.
- Leaving scope questions unanswered indefinitely, which quietly converts whole areas of the program into untested ground.

## Done when

- Every asset class has an explicit touched, not-touched or blocked status with a reason.
- The gap list is ranked by impact with a concrete next action each, and parked scope questions are escalated.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne - recon and methodology resources](https://hackerone.com/blog)
