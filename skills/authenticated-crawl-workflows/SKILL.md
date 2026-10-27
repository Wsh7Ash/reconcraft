---
name: authenticated-crawl-workflows
description: "Crawl behind login using your own test accounts so role-gated surfaces appear in your inventory instead of hiding behind a redirect. Use when the interesting application areas sit behind authentication and your program rules allow testing with provided accounts"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [authentication, crawling, roles]
---

# Authenticated Crawl Workflows

> Crawl behind login using your own test accounts so role-gated surfaces appear in your inventory instead of hiding behind a redirect

**Use when:** the interesting application areas sit behind authentication and your program rules allow testing with provided accounts

**Avoid when:** you have no authorized account, where everything you can reach is necessarily the public surface only

## Procedure

1. Confirm which accounts you are authorized to use, creating your own registration where the program allows it.
2. Capture the login flow and session material once, then reuse it so every crawl starts from a known authenticated state.
3. Tag each crawl with the account and role that performed it, because results from different roles are not comparable otherwise.
4. Detect session expiry during the run by watching for unexpected redirects to login, and re-authenticate instead of recording noise.
5. Compare role outputs afterwards to see which routes and objects differ between privilege levels.
6. Persist role-labelled route sets so later authorization testing has a concrete map of who can reach what.

## Signals

- A run's redirect rate suddenly spikes to login pages, which means the session expired rather than the pages disappearing.
- The same path returns different structures for two roles, indicating server-side authorization worth testing carefully.
- An account begins receiving rate limits or lockouts, which is your cue to slow down and switch accounts deliberately.
- Sensitive routes appear in only one role's crawl, which is exactly the boundary you want to document.

## Patterns

**1. Run label**

```text
run=crawl-014 role=member account=tester+member@example.test pages=1204 redirect_to_login=0
```

**2. Role diff**

```text
route            | member | admin
/admin/settings  | 403    | 200
/export          | 404    | 200
-> differences become authorization test cases
```

**3. Session check**

```text
if response redirects to /login mid-run: re-authenticate, then resume frontier from checkpoint
```

## Pitfalls

- Crawling with a privileged account only, which hides the lower-privilege view that usually contains the bug.
- Recording 403 responses as missing pages, so role-gated surface vanishes from your inventory.
- Running two accounts concurrently without labelling, making it impossible to say which role saw which route.

## Done when

- Every crawl run records its account and role, and expired sessions are handled rather than misrecorded.
- Role-labelled route sets exist and their differences are queued as authorization test cases.

## References

- [OWASP Web Security Testing Guide - authentication testing](https://owasp.org/www-project-web-security-testing-guide/)
- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
