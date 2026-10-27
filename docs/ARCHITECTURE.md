# Architecture

## Goals

1. **One source of truth.** Skills are authored as Python data; Markdown files are generated. A test asserts committed files match a fresh render, so the two can never disagree.
2. **Validation is a first-class gate.** Every quality floor lives in `validate.py` and is enforced by both the CLI and the test suite.
3. **No runtime dependencies.** Standard library only, so the pack runs anywhere Python 3.10+ exists.

## Components

```text
src/reconcraft/
├─ corpus/           authored skill data (source of truth)
│  ├─ __init__.py    PACK metadata + loads part1..part3
│  ├─ part1.py       skills 1-17
│  ├─ part2.py       skills 18-34
│  └─ part3.py       skills 35-50
├─ model.py          Skill dataclass + strict dict loading
├─ render.py         deterministic SKILL.md + pack.json + results writer
├─ validate.py       every rule, one place
└─ cli.py            validate / list / show / search / build / plan
```

### Data flow

```text
part1..part3 (dicts)
      │  skill_from_dict()  -- shape check, rejects missing/empty fields
      ▼
   Skill (frozen dataclass)
      │
      ├─ render_skill(pack, skill) ──► skills/<slug>/SKILL.md
      │                                    │
      │                                    ├─ sha256 ──► pack.json
      │                                    └─ diff vs committed file = test
      │
      ├─ validate_pack(pack, skills) ──► [Issue] ──► CLI exit code
      │
      └─ cli commands (list/show/search/plan) read the same objects
```

## The renderer

`render_skill` is a pure function: given the same pack metadata and skill, it produces byte-identical output. It emits:

```text
---                      YAML-ish front matter (name, description, pack,
                         version, category, tags) with a JSON-quoted
                         description containing an explicit "Use when" clause
---
# Title
> Summary
**Use when:** ...   **Avoid when:** ...
## Procedure        numbered, 6+ entries
## Signals          bullets, 4+
## Patterns         fenced text blocks with labels, 3+
## Pitfalls         bullets, 3+
## Done when        bullets, 2+
## References       canonical [label](https://...) links, 1+
```

`build_pack` writes all skills, then `pack.json` (name, version, runtime, per-skill path/tags/meta/sha256) and the `results/` reports. It returns the written paths with digests so callers can assert.

## The validator

Rules fall into three families:

| Family | Examples |
|---|---|
| Structure | required sections, front-matter fields, slug/tag format, reference format, pack `meta_keys` |
| Strength | steps >= 6, signals >= 4, patterns >= 3, pitfalls >= 3, done-when >= 2, refs >= 1, words >= 180 |
| Hygiene | no `TODO`/`FIXME`/`TBD`/placeholder tokens, no machine-local paths, unique slugs and titles, exact skill count, regex validity for verification patterns |

`validate` also compares each file on disk against a fresh render (`file-missing`, `file-drift`), so a hand-edited `SKILL.md` fails the gate.

## The plan command

`plan` is the only domain-specific command in the harness:

1. Load a JSON profile (`target`, `assets`).
2. Keep skills whose declared `assets` intersect the profile's, optionally filtered by `--phase`.
3. Sort by the fixed phase order `scope → enumerate → discover → fingerprint → validate → document`.
4. Emit either a Markdown run sheet or `--json` for tooling.

`--json` output shape: `{target, assets, count, plan: [{phase, skill, title}]}`.

## Testing strategy

| Test | Protects |
|---|---|
| corpus shape, count, uniqueness | the "50 unique skills" promise |
| full rule pass | the "100% valid" promise |
| byte-identical regeneration | committed files == source of truth |
| `pack.json` hash check | manifest integrity |
| drift detection test | the gate actually catches tampering |
| CLI subprocess tests | documented flags, output and exit codes |

## Design decisions

- **Generated files are committed.** Readers of a skill repository should see `SKILL.md` without running a build; CI proves they are current.
- **Three corpus files instead of fifty.** One file per skill would make the repository unreadable to navigate and expensive to review; one giant file is unreviewable. Three balanced parts keep diffs local.
- **Rules live in one module.** Both the CLI and the tests import the same constants, so a threshold change cannot silently diverge from what CI enforces.
- **No network at any point.** The pack is pure local computation, which keeps tests deterministic and the tool usable in air-gapped environments.
