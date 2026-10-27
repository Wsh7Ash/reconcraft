---
name: recon-snapshot-capture
description: "Capture a reproducible snapshot of everything you found so later runs can diff against it instead of starting from zero. Use when you finish a recon pass and want the result to remain useful weeks later when the program changes"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [snapshots, reproducibility, notes]
---

# Recon Snapshot Capture

> Capture a reproducible snapshot of everything you found so later runs can diff against it instead of starting from zero

**Use when:** you finish a recon pass and want the result to remain useful weeks later when the program changes

**Avoid when:** you are doing an exploratory first look where freezing a format would only slow you down

## Procedure

1. Fix the schema first: hosts, endpoints, services, cloud assets and third-party dependencies, each with stable identifiers.
2. Stamp every record with capture time, method and the scope verdict that authorized collecting it.
3. Store the snapshot as plain diffable text so any tool, or any reviewer, can compare two runs.
4. Include your tool versions and configuration, since a changed tool is a changed measurement instrument.
5. Keep raw outputs alongside the normalized snapshot, so surprising results can be re-examined rather than trusted.
6. Name snapshots by date and engagement so a later report can cite exactly which state it observed.

## Signals

- Two runs disagree about a host count and you cannot tell which configuration produced which number.
- A reviewer asks when you observed something and your notes only say recently.
- Raw output was deleted after normalization and a disputed result can no longer be checked.
- Tool defaults changed between runs, silently altering what your scan actually did.

## Patterns

**1. Snapshot header**

```text
engagement=example-bounty captured=2026-10-27T10:12Z
tool=dns-resolver x.y config=rate-5rps scope_verdict=allow-list-v2
```

**2. Record row**

```text
kind=host id=app-01 name=app.example.com method=dns-resolve scope=allow
```

**3. Raw store**

```text
raw/dns-2026-10-27.txt  raw/ct-2026-10-27.jsonl  normalized/snapshot.md
```

## Pitfalls

- Storing only prose summaries, which cannot be diffed and become archaeology within a month.
- Recording tool names without versions, so a behaviour change looks like a target change.
- Skipping the scope verdict, making it impossible to show why collecting a given record was authorized.

## Done when

- A dated snapshot exists in a diffable format with method, tool version and scope verdict on every record.
- Raw outputs are retained alongside it, and a test diff against the previous snapshot runs cleanly.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackerOne - reporting and documentation practices](https://hackerone.com/blog)
