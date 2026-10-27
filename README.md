# reconcraft

**50 validated bug-bounty reconnaissance skills, plus a CLI that turns a target profile into an ordered run sheet.**

## The problem

Reconnaissance knowledge for bug bounty lives in scattered blog posts, bookmarks and half-remembered checklists. Agents and humans both lose time re-deciding the same things: what to enumerate first, what counts as a real subdomain, when a response is a soft-404, what to hand off next. Generic "recon tips" lists do not help either, because nothing in them is checkable — you cannot tell whether a skill is complete, current or even followed.

## What this repo does

`reconcraft` is a corpus of **50 unique skills** organised into the six phases of an authorized recon engagement — `scope → enumerate → discover → fingerprint → validate → document` — with a validator that enforces structural and quality floors on every skill, and a CLI that uses the corpus instead of just storing it.

Every skill is a self-contained procedure with a summary, use/avoid guidance, a numbered procedure, observable signals, concrete patterns, pitfalls and completion criteria.

### Key features

- **50 skills, all validated**: `validate` enforces 6+ steps, 4+ signals, 3+ patterns, 3+ pitfalls, 180+ words, canonical `https` references, no placeholder tokens, no machine-local paths, unique slugs and titles, and byte-identical agreement with the files on disk.
- **`plan`**: turns a JSON target profile (target + asset classes) into an ordered, phase-grouped run sheet.
- **`validate`**: the "50/50 valid" gate. Exits non-zero on any violation, with `--json` for CI.
- **`build`**: deterministically regenerates `skills/`, `pack.json` (SHA-256 per skill) and `results/`.
- **`list` / `show` / `search`**: browse and search the corpus locally, no network required.
- **Zero runtime dependencies**: Python standard library only; `pytest` is the single dev dependency.

### Terminal example

```console
$ python -m reconcraft validate
reconcraft: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https

$ python -m reconcraft plan --profile examples/target-profile.json | head -8
# Recon plan - example-bounty.demo
Assets: api, web
Skills selected: 50 of 50

## scope
1. `program-scope-parsing` - Program Scope Parsing
   Turn a bug-bounty program's prose scope rules into an explicit allow, deny and unlisted asset list that can be checked before every request
2. `asset-inventory-baselining` - Asset Inventory Baselining
   ...

$ python -m reconcraft search wildcard dns
 14  wildcard-dns-handling                       Wildcard DNS Handling
  6  passive-subdomain-discovery                Passive Subdomain Discovery
  ...
```

## Architecture

```text
corpus (Python dicts)  --skill_from_dict-->  Skill dataclasses
        |                                          |
        |                    +---------------------+
        v                    v
   render.py  --SKILL.md-->  skills/<slug>/SKILL.md  + pack.json (sha256)
        |                    results/catalog.md, results/validation.json
        v
   validate.py  --rules-->  Issue list  -->  CLI exit code (0 = 50/50 valid)
```

- **Corpus** (`src/reconcraft/corpus/`): the source of truth, three readable files of authored skill dicts.
- **Model** (`model.py`): typed `Skill` shape plus strict dict validation.
- **Render** (`render.py`): pure, deterministic renderer and pack builder — same input, byte-identical output.
- **Validate** (`validate.py`): all structural, strength and hygiene rules in one place.
- **CLI** (`cli.py`): shared subcommands plus reconcraft's domain command `plan`.

Generated files are committed; tests assert committed files match a fresh render, so drift is a test failure rather than a silent surprise.

## Requirements

- Python 3.10+ (tested on 3.14)
- `pytest` for the test suite

## Installation

```shell
git clone https://github.com/Wsh7Ash/reconcraft.git
cd reconcraft
python -m pip install -e ".[dev]"
```

Or run it without installing anything:

```shell
PYTHONPATH=src python -m reconcraft --help
```

## Quick start

```shell
python -m reconcraft validate                 # expect: 50/50 skills valid
python -m reconcraft list | head              # browse the corpus
python -m reconcraft show wildcard-dns-handling
python -m reconcraft plan --profile examples/target-profile.json
```

## Usage

```shell
# Search the corpus
python -m reconcraft search subdomain takeover

# Inspect one skill in full
python -m reconcraft show dns-record-triage

# Restrict a listing to a phase or a tag
python -m reconcraft list --phase enumerate
python -m reconcraft list --tag dns

# CI-friendly validation
python -m reconcraft validate --json

# Regenerate all committed artifacts
python -m reconcraft build
```

Target profile format (`examples/target-profile.json`):

```json
{
  "target": "example-bounty.demo",
  "assets": ["web", "api"],
  "notes": "Synthetic target used only to demonstrate the planner"
}
```

`assets` accepts `web`, `api` and `all`; each skill declares which asset classes it applies to.

## Configuration

No configuration files and no network access. Behaviour is controlled by flags: `--phase`, `--tag`, `--json`, `--profile`, `--root`.

## Testing

```shell
PYTHONPATH=src python -m pytest -q
```

The suite covers corpus shape and uniqueness, the full rule set, byte-identical regeneration, hash agreement with `pack.json`, drift detection, and every CLI command including exit codes.

## Project structure

```text
reconcraft/
├─ README.md                  this file
├─ RESULTS.md                 what was actually executed
├─ SECURITY.md                authorized-use policy
├─ CHANGELOG.md  CONTRIBUTING.md  LICENSE  .gitignore
├─ pack.json                  manifest: 50 skills + sha256 each
├─ skills/<slug>/SKILL.md     50 generated skills
├─ src/reconcraft/
│  ├─ corpus/                 authored corpus (part1..part3)
│  ├─ model.py  render.py  validate.py  cli.py
├─ tests/test_corpus.py
├─ docs/ARCHITECTURE.md  docs/USAGE.md  docs/PROJECT_SPEC.md
├─ examples/target-profile.json
├─ results/                   validation.json, catalog.md, plan.md, ...
└─ .github/workflows/ci.yml
```

## Limitations

- This is a **knowledge corpus and planner**, not a scanner: `reconcraft` never sends network traffic.
- Validation proves structure and completeness, not factual correctness of every claim; references are provided for verification.
- The plan is phase-ordered, not time-estimated; it does not know your rate budget.
- Skill coverage targets web/API recon; wireless, mobile-device and physical testing are out of scope.

## Roadmap

- `plan --budget` to attach a time or request budget to the run sheet.
- SARIF output for `validate`, so findings land in code scanning UIs.
- A diff command that compares two `results/` snapshots from different runs.

## Security notes

All skills assume **authorized testing**: your own systems or a program you have permission to test. See [SECURITY.md](SECURITY.md). The corpus contains no weaponized payloads and no live target data.

## Credits

Structure and skill-file conventions were learned from the author's own collections: [Claude-Red](https://github.com/Wsh7Ash/Claude-Red) (SKILL.md format, category layout) and [awesome-bug-bounty](https://github.com/Wsh7Ash/awesome-bug-bounty) (topic coverage, resource curation).

## License

MIT — see [LICENSE](LICENSE).
