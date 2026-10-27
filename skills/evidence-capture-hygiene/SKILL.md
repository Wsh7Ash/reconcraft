---
name: evidence-capture-hygiene
description: "Collect request and response evidence that proves your finding while keeping secrets, cookies and personal data out of it. Use when you are assembling proof for a report, a screenshot or a HAR file attached to a submission"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [evidence, redaction, reporting]
---

# Evidence Capture Hygiene

> Collect request and response evidence that proves your finding while keeping secrets, cookies and personal data out of it

**Use when:** you are assembling proof for a report, a screenshot or a HAR file attached to a submission

**Avoid when:** you are still exploring privately and nothing will leave your machine yet

## Procedure

1. Capture the full request and response with timestamps, keeping the minimal set that proves the behaviour you claim.
2. Redact session tokens, cookies, authorization headers and any third-party personal data before the artifact leaves your machine.
3. Preserve the structure a reviewer needs: header names, flags, status codes and the shape of values stay intact.
4. Label each artifact with the endpoint, account role and step in reproduction so it can be read without your notes.
5. Store originals privately and share only redacted copies, keeping the mapping between them local.
6. Re-check the redacted artifact once more, since one overlooked header is enough to leak a live session.

## Signals

- A HAR file contains a cookie header captured from your own authenticated session.
- A screenshot shows an email address or account identifier belonging to someone other than your test account.
- A request body contains a token that appears again in a query string, needing redaction in two places.
- The evidence includes a third-party script response carrying an unrelated vendor's data.

## Patterns

**1. Redact keep**

```text
Authorization: Bearer <REDACTED>   Cookie: session=<REDACTED>
keep: header name, scheme, length class, HttpOnly and Secure flags
```

**2. Artifact label**

```text
artifact=03-idor-response.http role=member account=tester@example.test step=3-of-4
```

**3. Final check**

```text
scan artifact for: bearer tokens, cookies, emails, phone numbers, card-shaped digits
```

## Pitfalls

- Attaching a raw HAR to a report, which routinely carries live session material the whole triage team can see.
- Screenshotting a page that contains another user's data, converting your report into a disclosure problem.
- Redacting only in the visible request and forgetting headers that the tool appends automatically.

## Done when

- The artifact you share passes a final scan for tokens, cookies and personal identifiers.
- Each artifact carries its reproduction label, and unredacted originals stay on your machine only.

## References

- [HackerOne - report quality guidance](https://hackerone.com/blog)
- [PortSwigger - capturing evidence with proxy tooling](https://portswigger.net/web-security)
