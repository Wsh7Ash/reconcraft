---
name: active-subdomain-bruteforce
description: "Confirm which candidate hostnames really exist by resolving them against authorized infrastructure while handling wildcard answers correctly. Use when you hold a wordlist or candidate set and need verified live subdomains for an in-scope domain you are authorized to test"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [subdomains, dns, enumeration]
---

# Active Subdomain Bruteforce

> Confirm which candidate hostnames really exist by resolving them against authorized infrastructure while handling wildcard answers correctly

**Use when:** you hold a wordlist or candidate set and need verified live subdomains for an in-scope domain you are authorized to test

**Avoid when:** the program restricts active enumeration, or wildcard DNS is unresolved and would turn every guess into a false positive

## Procedure

1. Confirm the domain is in scope and note the rate and technique limits the program states for active enumeration.
2. Probe a random label first to detect wildcard DNS and wildcard certificate behaviour before trusting any result.
3. Resolve your candidate list through at least two resolver paths so a single resolver outage does not decide your results.
4. Group answers by record type and canonical name, because many labels often CNAME to one shared platform endpoint.
5. Mark every hit with its probe method so a later reviewer can tell a confirmed answer from a guess.
6. Persist only confirmed hosts plus the wildcard status of each domain into your inventory snapshot.

## Signals

- Every random label resolves to the same address, which means the domain is wildcarded and needs answer comparison to filter.
- Two resolvers disagree about a hostname, which usually indicates split-horizon DNS rather than a discovery.
- Newly found hosts CNAME into a cloud provider zone that the program does not mention in scope.
- A hostname answers only over one resolver path, hinting at internal or split-horizon records you should not chase.

## Patterns

**1. Wildcard probe**

```text
query: xyz-random-12345.domain.tld
answer: 203.0.113.10  -> wildcard present, require answer-diff filtering
answer: NXDOMAIN      -> wildcard absent, plain answers are real
```

**2. Result grouping**

```text
host -> cname -> final A/AAAA
cdn.example.net -> cluster7.provider.net -> shared edge addresses
shared suffix across many hosts = platform, not unique application
```

**3. Confirmation record**

```text
host=app.example.com method=dns-resolve sources=resolverA,resolverB wildcard=no status=confirmed
```

## Pitfalls

- Reporting hundreds of hosts from a wildcard domain without filtering, which buries the real surface under noise.
- Running the wordlist at full speed against production DNS and tripping the rate rules you agreed to.
- Treating a single resolver's timeout as proof a host does not exist, when it may only reflect that resolver's view.

## Done when

- Wildcard status is known for every enumerated domain and only answer-confirmed hosts are kept.
- Each confirmed host records how it was confirmed, and the result is merged into the dated inventory snapshot.

## References

- [HackTricks - DNS enumeration](https://book.hacktricks.xyz/)
- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
