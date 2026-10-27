# Security Policy

## Authorized use only

`reconcraft` is a knowledge corpus and planning tool for **authorized** security testing: systems you own, or programs whose rules explicitly permit you to test them. The software itself performs no network requests — it renders, validates and plans locally.

The skills describe reconnaissance methodology. They are not instructions for attacking systems you have no permission to touch, and using them against third-party infrastructure without authorization is unlawful in most jurisdictions.

## Scope discipline is built into the corpus

The first four skills of the pack exist precisely to keep work in bounds:

1. `program-scope-parsing` — every asset resolves to ALLOW, DENY or UNLISTED, with deny taking precedence.
2. `asset-inventory-baselining` — nothing gets tested before it is inventoried and confirmed.
3. `authorization-proof-checklist` — written permission, technique mapping and a stop condition.
4. `testing-window-and-rate-discipline` — rate ceilings and allowed windows before any active work.

A `plan` produced by the CLI always includes those phases first.

## What this repository contains

- Methodology, checklists and diagnostic patterns for defensive and authorized testing.
- No weaponized exploit payloads, no credential harvesting techniques, no phishing material, no evasion guidance.
- No live target data, no credentials, no personal data. The example target (`example-bounty.demo`) is synthetic.

## Reporting a vulnerability in this project

If you find a defect in `reconcraft` itself (for example, a validation bypass that lets a malformed skill pass the gate), please open a private security advisory on the repository or contact the maintainer through GitHub. Do not publish exploit details before a fix is available.

## Scope of this project's own testing

There is no hosted service, no API and no telemetry. Nothing to attack, nothing phoning home.
