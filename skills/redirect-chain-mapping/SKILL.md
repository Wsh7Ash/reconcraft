---
name: redirect-chain-mapping
description: "Trace every redirect hop, including client-side and protocol-level redirects, to see where navigation actually ends. Use when an entry point hands off through one or more redirects, or you want to confirm where unvalidated redirects ultimately lead"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [redirects, http, mapping]
---

# Redirect Chain Mapping

> Trace every redirect hop, including client-side and protocol-level redirects, to see where navigation actually ends

**Use when:** an entry point hands off through one or more redirects, or you want to confirm where unvalidated redirects ultimately lead

**Avoid when:** the endpoint returns directly with no redirect behaviour to analyze

## Procedure

1. Follow redirects manually one hop at a time, recording status, location header and set-cookie at each step.
2. Note protocol changes, host changes and whether any hop crosses into a third-party domain.
3. Capture client-side redirects that live in scripts or meta tags, which a plain HTTP follow would hide.
4. Identify where user-controlled input enters the chain, since that determines whether a redirect is exploitable.
5. Map the full chain in order with timings, so intermittent or conditional hops become visible.
6. Summarize the final destination and the trust boundaries crossed along the way for your report.

## Signals

- A hop passes an unvalidated parameter straight into the next location value.
- The chain crosses from the vendor domain into a third party, which is a trust-boundary note.
- Cookies are set on one hop and consumed on another, showing how the session is handed around.
- A meta refresh appears where an HTTP redirect was expected, meaning automated tools silently miss it.

## Patterns

**1. Chain record**

```text
1) 302 Location: /login?next=/checkout
2) 200 login page
3) 302 Location: /checkout  (post-auth)
crosses: none, third-party: none
```

**2. Input entry**

```text
GET /out?url=https://evil.example -> 302 Location: https://evil.example
input flows into target -> candidate open redirect, verify with your own host
```

**3. Hop timing**

```text
hop1=143ms hop2=18ms hop3=9ms total=170ms (conditional redirect visible in timing)
```

## Pitfalls

- Letting the client auto-follow, which merges hops and hides status codes you needed to document.
- Ignoring meta and script redirects, which real users follow but scanners never see.
- Recording only the final destination, so a redirect that leaks a token mid-chain disappears from your notes.

## Done when

- Every hop is recorded with status, target and cookies, including any client-side navigation.
- Trust boundaries and input entry points along the chain are documented for the report.

## References

- [RFC 9110 - redirection status codes](https://www.rfc-editor.org/rfc/rfc9110)
- [PortSwigger - open redirection topics](https://portswigger.net/web-security)
