---
name: shared-hosting-and-ip-attribution
description: "Decide whether an address genuinely belongs to the program before you scan it, avoiding shared CDNs, clouds and reverse proxies. Use when an IP or hostname appears in your results and you need to know whose infrastructure it really is before sending any traffic"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [attribution, infrastructure, scope]
---

# Shared Hosting and IP Attribution

> Decide whether an address genuinely belongs to the program before you scan it, avoiding shared CDNs, clouds and reverse proxies

**Use when:** an IP or hostname appears in your results and you need to know whose infrastructure it really is before sending any traffic

**Avoid when:** the asset is a hostname already confirmed as vendor-owned, where attribution adds no new information

## Procedure

1. Resolve the hostname and record whether the answer is an origin address, a CDN edge or a cloud load balancer front end.
2. Check reverse records and certificate subjects for the address, which usually name the operating platform rather than your target.
3. Compare the address against known provider ranges to spot shared infrastructure that hosts thousands of unrelated tenants.
4. Look for co-hosted hostnames on the same address through public indexes, since neighbours on shared edge IPs are usually unrelated.
5. Confirm ownership with at least two independent signals before treating the address as in-scope test surface.
6. Record the verdict as vendor-owned, shared-platform or third-party so later scans can skip what they must not touch.

## Signals

- The address resolves to a CDN edge serving many unrelated hostnames found through public datasets.
- Reverse records name a cloud provider rather than the vendor, which means the IP is a shared entry point.
- Certificate subjects on the address list hostnames from several different organizations.
- Scanning the address would reach other tenants, which is the clearest possible sign to stop.

## Patterns

**1. Ownership signals**

```text
signal A: reverse record names the vendor's own netblock
signal B: certificate SANs contain only vendor domains
signal C: vendor documentation states the address range
>= 2 signals -> vendor-owned
```

**2. Shared verdict**

```text
CDN edge + many foreign hostnames -> SHARED, scan by hostname only
cloud LB + no ownership signal     -> UNVERIFIED, ask before touching
```

**3. Inventory note**

```text
host=api.example.com ip=203.0.113.10 type=cdn-edge scope=hostname-only
```

## Pitfalls

- Scanning a shared CDN address, which sends traffic to unrelated tenants and instantly ends your engagement.
- Trusting reverse DNS alone, since it is trivially spoofable and often simply names the hosting provider.
- Treating an unverified cloud address as in scope because the hostname in front of it was in scope.

## Done when

- Every address you plan to touch carries a vendor-owned verdict backed by at least two independent signals.
- Shared or unverified addresses are marked hostname-only in the inventory so no future tool scans them blindly.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [Shodan - understanding shared infrastructure](https://www.shodan.io/)
