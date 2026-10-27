---
name: content-discovery-with-wordlists
description: "Find undisclosed paths and endpoints with a controlled wordlist crawl that filters noise and respects your rate ceiling. Use when you know the application host and want directories, files or routes that are not linked from any page you have seen"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [content-discovery, wordlist, paths]
---

# Content Discovery with Wordlists

> Find undisclosed paths and endpoints with a controlled wordlist crawl that filters noise and respects your rate ceiling

**Use when:** you know the application host and want directories, files or routes that are not linked from any page you have seen

**Avoid when:** the application exposes a documented route map or schema, where guessing paths adds noise instead of coverage

## Procedure

1. Baseline the target first: fetch a known-good page and a guaranteed-missing path so you know what real and fake responses look like.
2. Choose a wordlist sized for the program's rate rules and prioritize words drawn from the application's own vocabulary.
3. Run discovery in a single controlled pass, recording status, length, redirect target and content hash for every response.
4. Filter soft-404s by comparing each candidate against the guaranteed-missing baseline rather than trusting status codes alone.
5. Group hits by directory prefix so one broken catch-all route does not drown the interesting findings.
6. Queue only confirmed, unique paths for deeper review and keep the raw output for later diffing.

## Signals

- A candidate returns the same body length and hash as your guaranteed-missing baseline, which marks a soft-404.
- Status 200 responses appear for a large fraction of the wordlist, which usually means a catch-all handler.
- Redirects land on a login page for many paths, which suggests an authentication wall rather than real content.
- One path returns a distinct length, content type or server header from everything else in its directory group.

## Patterns

**1. Baseline pair**

```text
GET /definitely-missing-xyz -> 200, len=9821, type=text/html, hash=aa41...
GET /known-good-page        -> 200, len=12033, type=text/html, hash=77de...
```

**2. Filter rule**

```text
candidate hash == missing-baseline hash -> discard as soft-404
candidate hash differs AND status not in (404,429) -> keep for review
```

**3. Result row**

```text
/admin/login  200  len=2311  hash=5f90  group=/admin  verdict=unique
```

## Pitfalls

- Trusting status codes alone on an application that returns 200 for everything, which inflates results with garbage.
- Running the largest wordlist you have against a small program, burning your rate budget on paths nobody could have hidden.
- Ignoring 429 responses and pushing through, which breaks the rate discipline you agreed to in an earlier skill.

## Done when

- The baseline pair is recorded and every kept path differs from the missing-path response on hash or content type.
- Raw output is stored for diffing, and confirmed paths are queued with their group prefix attached.

## References

- [PortSwigger - content discovery](https://portswigger.net/web-security/content-discovery)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
