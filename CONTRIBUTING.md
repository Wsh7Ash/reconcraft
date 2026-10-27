# Contributing

Thanks for helping improve `reconcraft`.

## Ground rules

- **Authorized-use scope only.** Contributions must stay defensive or methodology-focused: no weaponized payloads, no credential harvesting, no evasion or persistence techniques, no instructions for testing systems the reader does not own or have permission to test.
- **No live data.** Never commit real target names, hostnames, credentials, cookies, tokens or personal data. Synthetic examples only.
- **One skill, one job.** A skill must be a single self-contained procedure with a clear "use when" and "avoid when".

## Adding or editing a skill

1. Edit the corpus in `src/reconcraft/corpus/part1.py`–`part3.py` (the source of truth). Do **not** hand-edit `skills/**/SKILL.md`; generated files are overwritten and a drift test will fail.
2. Regenerate and check the gate:

   ```shell
   PYTHONPATH=src python -m reconcraft build
   PYTHONPATH=src python -m reconcraft validate   # must print 50/50
   PYTHONPATH=src python -m pytest -q
   ```

3. Keep counts honest: adding a skill to the pack requires removing or merging another to keep the corpus at 50, or raising `expected_skills` deliberately in `corpus/__init__.py` together with a note in the PR.

## Quality floor enforced by CI

| Rule | Floor |
|---|---|
| Steps / signals / patterns / pitfalls / done-when | 6 / 4 / 3 / 3 / 2 |
| Rendered words per skill | >= 180 |
| References | canonical `[label](https://...)`, >= 1 |
| Slugs and titles | unique, lowercase kebab-case |
| Hygiene | no placeholder tokens, no machine-local paths |

## Pull requests

- Keep one concern per PR (one skill family, one rule change, one CLI feature).
- Include the output of `validate` and `pytest` in the description.
- Update `CHANGELOG.md` and `RESULTS.md` when behaviour changes.
