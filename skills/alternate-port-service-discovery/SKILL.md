---
name: alternate-port-service-discovery
description: "Find additional services on vendor-owned addresses using careful, rate-limited probes that stay inside the authorized range. Use when your inventory has confirmed addresses and the program's rules permit service discovery on them"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [ports, services, discovery]
---

# Alternate Port Service Discovery

> Find additional services on vendor-owned addresses using careful, rate-limited probes that stay inside the authorized range

**Use when:** your inventory has confirmed addresses and the program's rules permit service discovery on them

**Avoid when:** the rules limit testing to web ports, or the addresses are shared platform endpoints rather than vendor-owned hosts

## Procedure

1. Re-read the program rules for permitted ports and techniques, and write the permitted set into your scanner configuration.
2. Run a targeted probe of common service ports against confirmed vendor-owned addresses only, at the agreed rate.
3. Grab a short banner or handshake for each open port and classify the service from protocol behaviour, not the port number alone.
4. Separate vendor-operated services from provider-managed endpoints such as edge load balancers that must not be touched further.
5. Record each open port with service, version hints and the address it was seen on, then close the probe session cleanly.
6. Feed confirmed services back into inventory so later phases know which protocols and interfaces exist.

## Signals

- A non-standard port answers with a web application, which often means an unlisted admin or internal tool.
- A service banner names a version, giving you a defensible lead for configuration and patch review.
- Ports differ between two addresses that serve the same hostname, hinting at different tiers behind one front end.
- An unexpected management protocol appears, which should be reported for exposure rather than probed aggressively.

## Patterns

**1. Probe record**

```text
addr=203.0.113.10 port=8443 proto=tcp service=tls-http banner=nginx/1.24 scope=confirmed-owned
```

**2. Classification**

```text
port number -> hint only
protocol handshake -> truth (TLS certificate, HTTP response, SSH banner)
```

**3. Session log**

```text
range=203.0.113.10 ports=40 rate=5rps duration=92s open=3 outcome=within-limits
```

## Pitfalls

- Scanning the full internet-facing range of a cloud provider because one hostname resolved there.
- Assuming a service on a port belongs to the application when it is actually a provider health check endpoint.
- Running version-detection scripts at speed, which violates rate rules and looks like an attack to the vendor's monitoring.

## Done when

- Every open port you recorded came from a confirmed vendor-owned address within the permitted port set.
- Each service entry carries a protocol-based classification and is linked into the inventory snapshot.

## References

- [OWASP Web Security Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [HackTricks - service identification](https://book.hacktricks.xyz/)
