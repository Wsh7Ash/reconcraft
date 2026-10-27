# Project Spec — reconcraft

## Name

`reconcraft`

## Category

`bug-bounty-tooling`

## Target user

Bug-bounty hunters and security agents that run reconnaissance against programs they are authorized to test.

## Problem

Reconnaissance methodology is scattered across blog posts and checklists that are neither machine-checkable nor complete. Humans re-derive the same decisions every engagement; agents have no structured skill files to load, and nothing verifies that a "skill" is more than a heading.

## Solution

A corpus of 50 unique, validated recon skills organised into the six engagement phases, with a validator that enforces quality floors and a CLI that turns the corpus into an ordered run sheet.

## Core workflow

```text
author/edit corpus  ->  build  ->  skills/ + pack.json + results/
                                    |
                                    v
                          validate (50/50 gate)  ->  pytest  ->  CI
                                    |
                                    v
                       plan --profile target.json -> run sheet
```

## Must-have features

- 50 unique skills with unique slugs and titles, covering scope, enumerate, discover, fingerprint, validate, document.
- Validator with structural, strength and hygiene rules; exit `0` only at 50/50.
- Deterministic renderer; committed files proven in sync by tests.
- `plan` producing a phase-ordered run sheet from a JSON profile.
- `list`, `show`, `search`, `build` for browsing and regeneration.
- Zero runtime dependencies.

## Nice-to-have (not built)

- Time/request budgets on plans, SARIF output, snapshot diffing.

## Stack

Python 3.10+ standard library; `pytest` as the only dev dependency.

## Test strategy

`tests/test_corpus.py` — 16 tests: corpus shape and count, uniqueness, full rule pass, phase balance, word floor, hygiene scan, byte-identical regeneration, `pack.json` hash agreement, drift detection, and CLI subprocess behaviour (exit codes and `--json` payloads).

## Demo / result strategy

- `results/validation.txt` — the `50/50 valid` gate output.
- `results/validation.json` — machine-readable report with floors.
- `results/plan.md` — a full run sheet from `examples/target-profile.json`.
- `results/catalog.md` — the 50-row skill catalog.
- `results/search-example.txt` — ranked search output.

## Safety considerations

- The tool performs **no network I/O**; it plans and documents, it does not scan.
- Skills assume authorized testing only and carry an explicit scope/authorization phase as their first four entries.
- No live target data, credentials or personal data is stored in the repository.

## Definition of done

- [x] `python -m reconcraft validate` → `50/50 skills valid`, exit 0.
- [x] `python -m pytest -q` → all tests pass.
- [x] Committed `skills/` and `pack.json` match a fresh build.
- [x] README, ARCHITECTURE, USAGE, SECURITY, RESULTS, CI present.
- [x] Secret scan clean; published to GitHub as a public repository.
