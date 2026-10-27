---
name: program-scope-parsing
description: "Turn a bug-bounty program's prose scope rules into an explicit allow, deny and unlisted asset list that can be checked before every request. Use when you start a new program, the scope page changes, or an agent needs a machine-checkable in-scope verdict before it sends traffic"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [scope, program, triage]
---

# Program Scope Parsing

> Turn a bug-bounty program's prose scope rules into an explicit allow, deny and unlisted asset list that can be checked before every request

**Use when:** you start a new program, the scope page changes, or an agent needs a machine-checkable in-scope verdict before it sends traffic

**Avoid when:** the program already publishes a machine-readable asset list you have imported once for a single short engagement

## Procedure

1. Copy the scope section verbatim into your notes and keep the program URL and today's date next to it, because scope text is versioned by the vendor over time.
2. Split every line into one of four buckets: in-scope asset, explicitly out-of-scope asset, wildcard or pattern rule, and prose condition such as third-party services.
3. Normalize host patterns into a literal form so `*.example.com` becomes a suffix rule and `example.com` stays an exact host rule with no implicit subdomains.
4. Record the testing constraints that change how you work: rate limits, forbidden techniques, social-engineering rules and the disclosure channel.
5. Write the resulting allow and deny rules into a file your tooling can read, so a skipped manual check still cannot produce an out-of-scope request.
6. Re-run the parse whenever the program updates its policy page and diff the two versions before your next test session.

## Signals

- The policy page lists assets in three places (scope table, FAQ and rules prose) that disagree with each other.
- A wildcard covers a domain the program separately marks out of scope, which means deny must take precedence over allow.
- Scope mentions a cloud provider or CDN hostname that the vendor does not operate.
- The program text dates back several months while the asset inventory clearly changed recently.

## Patterns

**1. Four-bucket parse**

```text
in-scope:  api.example.com
in-scope:  *.example.com  (subdomains, exact apex excluded)
out:       admin.example.com
condition: third-party CDN assets excluded
```

**2. Rule precedence**

```text
deny(example.com) overrides allow(*.example.com)  -> verdict = DENY
allow(api.example.com) with no deny            -> verdict = ALLOW
no rule matched                                 -> verdict = UNLISTED (ask, do not test)
```

**3. Diff trigger**

```text
scope-v1.txt vs scope-v2.txt: +added-host, -removed-host, ~changed-condition
Any change requires a fresh verdict before the next request.
```

## Pitfalls

- Treating a wildcard as covering the apex domain; most programs mean subdomains only and testing the apex is then out of scope.
- Reading scope once at the start of a long engagement and never re-reading it after the vendor publishes a policy update.
- Assuming an unlisted asset is allowed; the correct verdict for anything unmatched is unlisted, which means ask before you test.

## Done when

- Every candidate asset resolves to ALLOW, DENY or UNLISTED with the source rule recorded next to it.
- The parsed rules live in a file your tools read, not only in prose notes, and a re-parse after a policy change produces a diff.

## References

- [HackerOne - How to read program scopes](https://hackerone.com/blog)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
