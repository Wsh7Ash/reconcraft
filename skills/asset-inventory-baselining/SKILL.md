---
name: asset-inventory-baselining
description: "Build a stable inventory of hosts, applications and interfaces for a program so later recon output can be diffed against a known starting point. Use when you begin sustained testing on a program and want a baseline that new subdomains, ports and endpoints can be compared against"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [inventory, baseline, scope]
---

# Asset Inventory Baselining

> Build a stable inventory of hosts, applications and interfaces for a program so later recon output can be diffed against a known starting point

**Use when:** you begin sustained testing on a program and want a baseline that new subdomains, ports and endpoints can be compared against

**Avoid when:** you are doing a one-off 30 minute check where a quick scan output is enough and nothing will be diffed later

## Procedure

1. List every asset type the program exposes: web hosts, API hosts, mobile backends, mail servers, cloud storage names and third-party services.
2. Record ownership signals for each entry: DNS answers, certificate subjects, provider accounts and any vendor statement that ties the asset to the program.
3. Give each asset a stable identifier so later runs can join on it even when ports, paths or IP addresses change.
4. Store one row per asset with owner, environment and last-confirmed date, in a format you can diff with ordinary tools.
5. Mark assets you cannot confirm as unverified rather than dropping them, so the gap is visible instead of silently lost.
6. Refresh the baseline on a fixed cadence and treat new rows as the highest-value recon leads you have.

## Signals

- A host appears in certificate transparency logs but in none of your prior snapshots.
- The same application is served from two hosts with different software versions behind them.
- Cloud storage or a CDN hostname is referenced by the application but absent from the program scope page.
- An asset you marked unverified months ago is still unconfirmed, which usually means it belongs to another team.

## Patterns

**1. Row shape**

```text
id | kind | name | owner | environment | last_confirmed | status
web | app-01 | shop.example.com | vendor | production | 2026-10-27 | confirmed
```

**2. Diff rule**

```text
new row      -> investigate first, it is attack surface you did not know about
missing row   -> confirm before celebrating, it may be decommissioned or firewalled
changed owner -> re-check scope verdict before any further testing
```

**3. Ownership check**

```text
DNS CNAME chain ends in a cloud provider  -> confirm the provider account is the program's
cert SAN list contains the host           -> strong signal of vendor control
```

## Pitfalls

- Recording only domain names and forgetting API hosts, mail endpoints and cloud storage that are equally in scope.
- Letting the baseline rot by adding one-off notes instead of updating the single inventory everyone reads.
- Deleting rows you cannot currently resolve; temporary DNS failures and outages would then look like clean removals.

## Done when

- The inventory covers every asset class the program exposes and each row carries an ownership signal and a last-confirmed date.
- A diff between two runs shows only real changes, and every new row has an owner in your notes before you test it.

## References

- [OWASP Web Security Testing Guide - Information Gathering](https://owasp.org/www-project-web-security-testing-guide/)
- [HackTricks - Pentesting methodology](https://book.hacktricks.xyz/)
