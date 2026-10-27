# Results

Reproducible evidence for the claims in `README.md`. Nothing below is marked PASS unless the command ran successfully in this repository.

## Environment

- OS: Windows (MSYS2 shell), Python 3.14
- Runtime: Python 3.10+ standard library, `pytest` as dev dependency
- Dependency manager: `pip` / `python -m pip install -e ".[dev]"`
- Network: none required at any point

## Validation performed

| Gate | Result |
|---|---|
| install (`pip install -e ".[dev]"`) | PASS |
| build (`reconcraft build`) | PASS (exit 0) |
| validation gate (`reconcraft validate`) | PASS — **50/50 skills valid** |
| unit tests (`pytest -q`) | PASS — **16 passed** |
| lint / type check | N/A (no linter configured for this stack) |
| demo run (`plan`, `search`) | PASS |
| secret scan | PASS (0 hits) |

## Commands executed

```shell
export PYTHONPATH=src
python -m reconcraft build                 # regenerates skills/, pack.json, results/
python -m reconcraft validate              # exit 0, prints 50/50
python -m pytest -q                        # 16 passed
python -m reconcraft plan --profile examples/target-profile.json > results/plan.md
python -m reconcraft search wildcard dns   > results/search-example.txt
grep -rniE "(ghp_|github_pat_|AKIA|BEGIN.*PRIVATE KEY|xox[baprs]-|sk-)" .   # no matches
```

## Observed result

```text
built 50 skills -> .../reconcraft/skills
reconcraft: 50/50 skills valid
  ok  steps>=6 signals>=4 patterns>=3 pitfalls>=3 words>=180 refs canonical https
................                                                         [100%]
16 passed
```

Corpus statistics measured from the rendered output:

```text
skills=50  min_words=360  max_words=503  total_words=20203
phase balance: scope=4 enumerate=11 discover=11 fingerprint=10 validate=8 document=6
unique slugs=50  unique titles=50
```

Every skill clears the 180-word floor by at least 180 words; the weakest skill is 360 words.

## Generated artifacts

- `results/validation.txt` — the validation gate output (`50/50 skills valid`).
- `results/validation.json` — machine-readable report with floors and issue list.
- `results/plan.md` — full phase-ordered run sheet from the example profile.
- `results/catalog.md` — 50-row catalog of slugs, titles and tags.
- `results/search-example.txt` — ranked keyword search output.
- `skills/*/SKILL.md` — the 50 rendered skills (committed, hash-verified in `pack.json`).

## Known limitations

- Validation proves structure, completeness and hygiene — not the factual accuracy of every methodology claim; references are provided so a reviewer can verify.
- The planner has no time or request budget model yet.
- Coverage targets web/API reconnaissance; wireless, device and physical testing are intentionally out of scope.
- Word-count floors are a proxy for substance, not a guarantee of usefulness; peer review of the corpus content is still worthwhile.
