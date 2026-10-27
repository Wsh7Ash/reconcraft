---
name: subdomain-permutation-enumeration
description: "Derive likely sibling hostnames from known ones using wordlists and mutators, then verify each candidate instead of guessing blindly. Use when you already have a few confirmed hostnames and want to predict neighbours such as staging, admin or regional variants"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [subdomains, wordlist, enumeration]
---

# Subdomain Permutation Enumeration

> Derive likely sibling hostnames from known ones using wordlists and mutators, then verify each candidate instead of guessing blindly

**Use when:** you already have a few confirmed hostnames and want to predict neighbours such as staging, admin or regional variants

**Avoid when:** the program's asset list is complete and published, making prediction unnecessary work with no new surface

## Procedure

1. Take your confirmed hosts as seeds and extract the naming conventions the vendor actually uses, such as region prefixes or environment suffixes.
2. Apply a small focused mutator set: environment words, ordinal variants, hyphen and digit insertion, and common service names.
3. Resolve or query each generated candidate and keep only answers that pass the same wildcard handling you used earlier.
4. Record which mutator produced each hit so you can retire the ones that never work for this vendor.
5. Check hits against scope before any HTTP request, since prediction frequently produces names the program never intended to expose.
6. Fold verified hits back into the seed list and stop when a full pass yields nothing new.

## Signals

- Two or three mutators account for every hit, which tells you the vendor's naming scheme is worth documenting.
- A predicted host resolves inside a cloud account rather than the vendor's own network.
- Naming patterns include environment words such as staging or uat, which often means weaker controls than production.
- A pass produces many candidates but zero new hosts, which means the naming space is likely exhausted.

## Patterns

**1. Mutator set**

```text
seeds: api.example.com, app.example.com
words: dev, stage, staging, test, uat, admin, internal, old, v2
joiners: -, ., digits 0-2
output: stage-api.example.com, api-v2.example.com
```

**2. Hit record**

```text
candidate=stage-api.example.com mutator=env-prefix method=dns-resolve scope=unlisted -> ask before testing
```

**3. Convergence**

```text
pass n: +4 hosts, pass n+1: +1 host, pass n+2: +0 hosts -> stop
```

## Pitfalls

- Generating thousands of candidates and blasting them through DNS, which wastes time and violates rate expectations.
- Predicting a hostname and testing it purely because it resolved; resolution is not a scope verdict.
- Never pruning mutators, so each run repeats work that already proved fruitless for this vendor.

## Done when

- New verified hosts are attributed to a specific mutator and checked against scope before use.
- The run terminates on a convergence rule rather than on an arbitrary candidate count.

## References

- [HackTricks - Subdomain enumeration](https://book.hacktricks.xyz/)
- [PayloadsAllTheThings - discovery resources](https://github.com/swisskyrepo/PayloadsAllTheThings)
