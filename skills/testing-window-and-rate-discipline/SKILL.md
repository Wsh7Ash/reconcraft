---
name: testing-window-and-rate-discipline
description: "Keep scanning and crawling inside the program's stated rate limits and business hours so your recon never degrades the target. Use when you run any active scan, crawler or brute force against an authorized target and need a predictable, polite traffic profile"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [rate-limit, stability, scanning]
---

# Testing Window and Rate Discipline

> Keep scanning and crawling inside the program's stated rate limits and business hours so your recon never degrades the target

**Use when:** you run any active scan, crawler or brute force against an authorized target and need a predictable, polite traffic profile

**Avoid when:** your work is purely passive OSINT gathered from public indexes with no traffic reaching the vendor's infrastructure

## Procedure

1. Read the program's rate and timing rules and write the numbers into your tool configuration instead of relying on tool defaults.
2. Set a global concurrency ceiling and a requests-per-second ceiling in one place so every tool inherits the same profile.
3. Prefer a single controlled pass over repeated full scans; store results and re-query them locally instead of re-hitting the target.
4. Schedule aggressive phases inside the window the vendor allows and keep continuous background work at a low, constant rate.
5. Watch for backpressure: rising latency or 429 responses are your signal to slow down, not to retry harder.
6. Log start time, request count and peak rate for each session so you can prove your traffic stayed inside the agreed envelope.

## Signals

- Latency climbs steadily during your session while the same endpoints respond quickly from another network.
- The target returns 429 or 503 with retry hints, which is backpressure rather than a vulnerability to press against.
- A monitoring team or the vendor contacts you about traffic, meaning your profile is already visible to them.
- Your tool configuration differs from the rate numbers written in the program rules.

## Patterns

**1. Ceiling config**

```text
global: concurrency=8, rate=5 rps, jitter=200ms
burst: disabled, retries=1, backoff=exponential
window: weekdays 09:00-17:00 vendor local time
```

**2. Backpressure response**

```text
429 or 503 received -> pause 30s, halve rate, resume once
second trigger      -> stop session and review configuration
```

**3. Session log**

```text
start=2026-10-27T10:00Z requests=4200 peak_rps=4.8 scope=api.example.com
outcome=within limits
```

## Pitfalls

- Turning on every scanner module at once, which multiplies your rate far beyond the number you configured in one place.
- Retrying aggressively on 429 responses, converting a polite scan into the denial-of-service behaviour the rules forbid.
- Running a crawl overnight in a time zone where the vendor's on-call team considers it a production incident window.

## Done when

- One configuration point sets concurrency and rate for every tool you use, and a dry run confirms it takes effect.
- Each session log shows request count and peak rate inside the program's stated envelope with no unexplained error bursts.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Bugcrowd - Researcher resources](https://www.bugcrowd.com/blog/)
