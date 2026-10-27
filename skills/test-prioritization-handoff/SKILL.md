---
name: test-prioritization-handoff
description: "Convert recon output into an ordered test plan that states what to test, in what order, and why each item ranks where it does. Use when recon is finished and you, or an agent, need a concrete plan for where testing time goes next"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [planning, handoff, priorities]
---

# Test Prioritization Handoff

> Convert recon output into an ordered test plan that states what to test, in what order, and why each item ranks where it does

**Use when:** recon is finished and you, or an agent, need a concrete plan for where testing time goes next

**Avoid when:** you have a single narrow target and no sequencing decision to make

## Procedure

1. List candidate targets from inventory with their asset class, exposure and current scope verdict.
2. Score each candidate on reachability, novelty, sensitivity of the data involved and how much recon already suggests.
3. Order the list so reachable, sensitive, lightly-examined targets come first and out-of-scope items are excluded entirely.
4. State for each entry what evidence you already hold and what question the next test should answer.
5. Hand off with explicit bounds: rate ceiling, forbidden techniques and the stop condition carried from earlier phases.
6. Review the plan after each testing session and re-rank, since the best evidence changes what should come next.

## Signals

- A candidate target has strong evidence attached but has never been requested, which means it should rank high.
- Your plan includes items with no evidence behind them, which usually means gut-feel ordering rather than reasoning.
- Items remain out of scope yet still appear in the plan, indicating the scope filter was not applied.
- Two sessions in a row skip the top of the plan, which means the ranking does not reflect reality.

## Patterns

**1. Score row**

```text
target=/export.csv class=export exposure=auth evidence=len-delta+param-discovery score=high order=1
```

**2. Handoff header**

```text
bounds: rate=5rps, techniques=allowed-set, stop=degradation-or-writes-outside-own-account
```

**3. Plan entry**

```text
1. /export.csv - question: does role enforcement apply on export?
evidence: discovered in bundle, never requested
```

## Pitfalls

- Shipping a plan with dozens of equally-ranked items, which is a list rather than a plan.
- Omitting bounds so the next session starts aggressive and violates the program's rate rules.
- Never re-ranking, so early guesses keep consuming time after evidence has moved on.

## Done when

- The plan is ordered with a stated reason and evidence per entry, and out-of-scope items are absent.
- Bounds and the stop condition travel with the plan, and re-ranking is scheduled after each session.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Bugcrowd - researcher methodology](https://www.bugcrowd.com/blog/)
