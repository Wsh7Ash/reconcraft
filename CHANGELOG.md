# Changelog

All notable changes to `reconcraft` are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow [SemVer](https://semver.org/).

## [1.0.0] - 2026-10-27

### Added

- Initial release: 50 unique reconnaissance skills across six phases
  (`scope`, `enumerate`, `discover`, `fingerprint`, `validate`, `document`).
- Validator with structural, strength and hygiene rules; `50/50 skills valid`
  gate with `--json` output for CI.
- Deterministic renderer and `build` command writing `skills/`,
  `pack.json` (SHA-256 per skill) and `results/`.
- CLI: `validate`, `list`, `show`, `search`, `build`, `plan`.
- `plan` — JSON target profile to phase-ordered run sheet.
- Test suite (16 tests) covering corpus shape, rules, regeneration, drift and
  every CLI command.
- CI workflow, docs (`ARCHITECTURE`, `USAGE`, `PROJECT_SPEC`), `SECURITY.md`.
