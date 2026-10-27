---
name: mail-infrastructure-mapping
description: "Map the mail systems a domain uses, including third-party senders, to understand account recovery and spoofing defens. Use when a program's flows depend on email, or you want to know which services can send mail as the vendor's domain"
pack: reconcraft
version: 1.0.0
category: bug-bounty-tooling
tags: [mail, dns, infrastructure]
---

# Mail Infrastructure Mapping

> Map the mail systems a domain uses, including third-party senders, to understand account recovery and spoofing defens

**Use when:** a program's flows depend on email, or you want to know which services can send mail as the vendor's domain

**Avoid when:** mail is irrelevant to the application and the program does not cover messaging infrastructure

## Procedure

1. Collect mail exchange records, their priorities and the hostnames they terminate at for every in-scope domain.
2. Read sender policy, domain key and DMARC policies to learn which senders are authorized and what happens on failure.
3. Follow include and redirect chains in the sender policy to enumerate every authorized sending service.
4. Note whether enforcement is strict or permissive, since that determines what a misconfiguration would actually allow.
5. Classify each sending service as vendor-operated or third-party, keeping third parties out of test scope.
6. Snapshot the records so changes, such as a new sender being authorized, appear in future diffs.

## Signals

- The sender policy authorizes a service the vendor no longer uses, which is a stale authorization worth reporting.
- DMARC policy is set to none, meaning reports exist but nothing is enforced against spoofed senders.
- Include chains reach a provider with a broad policy that covers many unrelated tenants.
- Mail exchange hosts live in a different domain, expanding your inventory of vendor dependencies.

## Patterns

**1. Record sweep**

```text
MX 10 mail.provider.net (priority 10)
TXT v=spf1 include:_spf.vendor-mail.net include:ses-sender.net -all
TXT v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com
```

**2. Sender list**

```text
authorized senders = {vendor-mail.net, ses-sender.net}
observed senders in headers -> compare against authorized set
```

**3. Snapshot row**

```text
domain | mx | spf | dmarc_p | captured
example.com | mail.provider.net | -all | quarantine | 2026-10-27
```

## Pitfalls

- Focusing only on mail exchange records while missing the sender policy includes, which name the actual sending services.
- Attempting to send mail as the domain to prove a point, which is outside what authorization to test confers.
- Forgetting that provider-owned mail hosts are third-party assets, even though the records live in vendor DNS.

## Done when

- Mail exchange, sender policy and DMARC are recorded per domain with all include chains followed to their ends.
- Authorized senders are listed and compared against observed ones, with third-party services marked out of scope.

## References

- [SPF receiver guidance](https://www.rfc-editor.org/rfc/rfc7208)
- [DMARC specification](https://www.rfc-editor.org/rfc/rfc7489)
