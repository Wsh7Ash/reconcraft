---
name: authorization-proof-checklist
description: "Assemble and keep the written permission, program rules and target mapping that prove every test you run is authorized. Use when you start testing, you add a new asset or technique, or an automated agent needs proof that a request is allowed before it fires"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [authorization, compliance, safety]
---

# Authorization Proof Checklist

> Assemble and keep the written permission, program rules and target mapping that prove every test you run is authorized

**Use when:** you start testing, you add a new asset or technique, or an automated agent needs proof that a request is allowed before it fires

**Avoid when:** you are only reading public documentation with no active requests, where no permission record is needed beyond the program page

## Procedure

1. Save the program policy, scope page and rules with a capture date, so you can show what was authorized at the time of a test.
2. Map each technique you plan to use to a rule line: which are allowed, which need prior approval and which are banned outright.
3. Confirm your test accounts, test data and any third-party data you touch are yours or synthetic, never a real customer's.
4. Write the emergency stop condition: the signal that makes you halt (service degradation, data beyond your own, unexpected write access).
5. Give every automated run an identity and a rate ceiling so its traffic can be recognized and stopped if it misbehaves.
6. Keep the record until the disclosure is closed, because scope questions usually arrive weeks after the testing finished.

## Signals

- A technique you planned is not mentioned in the rules at all, which means you must ask rather than assume.
- Your notes reference a target host that no longer appears on the scope page.
- An automated tool begins touching endpoints outside the allow list you configured.
- The program owner contacts you mid-test about traffic volume, which is a stop-and-confirm moment.

## Patterns

**1. Permission record**

```text
program: https://example.com/security
policy captured: 2026-10-27
allowed: authenticated testing with own account, rate-limited scanning
requires approval: account-takeover chaining, denial-of-service checks
banned: social engineering of staff, physical testing
```

**2. Stop condition**

```text
halt if: response times degrade, writes occur outside your account,
data belonging to other users appears, or traffic exceeds the stated limit
```

**3. Agent gate**

```text
before request: verdict in-scope AND technique allowed AND rate under ceiling
otherwise: log reason and skip
```

## Pitfalls

- Assuming a public asset is fair game because it was easy to find; public does not mean authorized.
- Letting a convenience tool run with default settings that ignore your allow list and rate ceiling.
- Testing with personal data you scraped earlier, which turns a permission question into a data-protection problem.

## Done when

- You can point to a captured policy, a technique-to-rule mapping and a written stop condition for the current engagement.
- Every automated run carries an identity and ceiling, and a dry run confirms out-of-scope requests are refused before they leave your machine.

## References

- [HackerOne - Responsible disclosure basics](https://hackerone.com/blog)
- [First.org CVSS - guidance on authorized testing context](https://www.first.org/cvss/)
