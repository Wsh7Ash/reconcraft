# Usage

## Commands

| Command | Purpose |
|---|---|
| `validate` | run every rule; check files on disk match the corpus |
| `list` | list skills, filterable by `--phase` / `--tag`, `--json` available |
| `show <slug>` | print one rendered `SKILL.md` |
| `search <terms...>` | rank skills by keyword frequency |
| `build` | regenerate `skills/`, `pack.json`, `results/` |
| `plan` | target profile → ordered recon run sheet |

Every command works through `python -m reconcraft` (or the `reconcraft` console script after `pip install -e .`).

## validate

```console
$ python -m reconcraft validate
reconcraft: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https
```

Exit code `0` means every skill passed every rule and every committed file matches a fresh render. Any violation prints one `FAIL <slug>: <rule>: <message>` line and exits `1`.

```console
$ python -m reconcraft validate --json | head -12
{
  "pack": "reconcraft",
  "checked": 50,
  "valid": 50,
  "passed": true,
  "floors": { "min_steps": 6, "min_signals": 4, ... },
  "issues": []
}
```

Flags:

- `--json` — machine-readable report (for CI).
- `--skip-files` — validate the authored corpus only, ignoring disk state (used by `build` before writing).
- `--root PATH` — validate a different checkout's generated files against this corpus.

## list

```console
$ python -m reconcraft list --phase enumerate
passive-subdomain-discovery                 enumerate   Passive Subdomain Discovery
active-subdomain-bruteforce                 enumerate   Active Subdomain Bruteforce
...
-- 11 skills
```

`--json` emits objects with `slug`, `title`, `tags`, `meta` and rendered `words`.

## show

```console
$ python -m reconcraft show wildcard-dns-handling
---
name: wildcard-dns-handling
description: "Detect wildcard and catch-all DNS responses early and ... Use when any subdomain enumeration ..."
...
```

Unknown slugs exit `1` with a message on stderr.

## search

```console
$ python -m reconcraft search wildcard dns
 14  wildcard-dns-handling                       Wildcard DNS Handling
  6  passive-subdomain-discovery                Passive Subdomain Discovery
```

Ranking counts occurrences across slug, title, summary, tags and steps; ties break alphabetically. No match → exit `1`.

## build

```console
$ python -m reconcraft build
built 50 skills -> .../reconcraft/skills
```

Writes `skills/<slug>/SKILL.md`, `pack.json` (with SHA-256 per skill), `results/catalog.md` and `results/validation.json`. Exits `1` if validation fails after writing, so CI catches both at once.

## plan

```console
$ python -m reconcraft plan --profile examples/target-profile.json
# Recon plan - example-bounty.demo
Assets: api, web
Skills selected: 50 of 50

## scope
1. `program-scope-parsing` - Program Scope Parsing
   Turn a bug-bounty program's prose scope rules into an explicit allow, deny and unlisted asset list...
...

Coverage by phase:
  scope         4 skills
  enumerate    11 skills
  discover     11 skills
  fingerprint  10 skills
  validate      8 skills
  document      6 skills
```

Profile format:

```json
{
  "target": "example-bounty.demo",
  "assets": ["web", "api"]
}
```

| Flag | Effect |
|---|---|
| `--profile PATH` | required; JSON file with `target` and `assets` |
| `--phase NAME` | restrict the plan to one phase |
| `--json` | emit `{target, assets, count, plan[]}` |

Asset values: `web`, `api`, `all` (a skill declaring `all` always matches).

## Using the skills with an agent

Each `skills/<slug>/SKILL.md` is a self-contained instruction file. Point your runtime's skill directory at this repository, or copy individual skill folders:

```text
your-agent/skills/reconcraft/wildcard-dns-handling/SKILL.md
```

The front matter carries `name`, a description with an explicit `Use when` clause, `pack`, `version`, `category` and `tags`, which is what a loader needs to decide when the skill applies.

## Validating your own edits

The corpus is the source of truth. After editing `part1.py`–`part3.py`:

```shell
python -m reconcraft build      # regenerate skills/, pack.json, results/
python -m reconcraft validate   # must print 50/50
PYTHONPATH=src python -m pytest -q
```

Editing a generated `SKILL.md` directly is a test failure by design.
