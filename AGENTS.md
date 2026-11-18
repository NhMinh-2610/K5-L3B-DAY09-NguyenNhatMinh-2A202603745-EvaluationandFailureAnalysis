# Repository Guidelines

## Project Structure & Module Organization

- `src/lab9/`: evaluation datasets, graders, judge calibration, statistics, gates, and evidence-generation CLIs.
- `src/lab8/`: instructor-provided agent, host, and SQLite implementation; preserve it unchanged.
- `src/tests/`: pytest suites, including `test_lab9_*.py` and Advanced checks.
- `src/config/` and `src/data/`: YAML policies/specifications, public claims, adversarial pack, and separate evaluation labels.
- `docs/`: taxonomy, trace analysis, judge audit, eval card, PRD, and PR evidence. `src/reports/` contains generated artifacts; `src/traces/` contains runtime traces.

## Build, Test, and Development Commands

Use Python 3.11–3.13 with an activated virtual environment. Run these commands from `src/`:

```bash
python -m pip install -r requirements.txt -r requirements-lab9.txt
python -m lab9.smoke
python -m lab9.evalset --check
python -m lab9.evalset --v2 --build
python -m pytest -q -m student -o addopts= -k lab9
python -m pytest -q -o addopts= tests/test_lab9_evalset.py
python -m lab9.advanced_evidence
```

These install dependencies, check setup, validate v1, build/check v2, run tests, and regenerate M5–M7 evidence. MockLLM and judge replay require no API key. See `TIEN_DO_LAB.md` for Windows commands.

## Coding Style & Naming Conventions

Use four-space Python indentation, `snake_case` functions/modules, and `PascalCase` evaluator classes. Follow existing type hints and short docstrings. No formatter or linter is configured. Keep metric IDs consistent across graders, YAML, and reports. Preserve LF endings for generated eval sets and labels through `.gitattributes`.

## Testing Guidelines

Use pytest, `test_lab9_*.py` filenames, and `test_*` functions. Mark student tests with `pytest.mark.student`; default pytest configuration excludes them, so retain the explicit command above. Select Core with `-k "lab9 and not advanced"` and Advanced with `-k advanced`.

No numeric coverage threshold is configured. Add regression tests for changed behavior and honest controls. Regression/trap gates should exit 1; successful aggregate evidence generation exits 0.

## Commit & Pull Request Guidelines

History uses imperative `feat:`, `docs:`, and `chore:` subjects. Keep commits focused. Reports are ignored: explicitly stage generated evidence with `git add -f src/reports`.

Open `starter/d09` → `main` within the personal fork. Include the problem/change, validation, seeded-regression exit-1 output, scorecard, A/A, and four trap verdicts; `docs/PR_LAB9.md` provides evidence. Require `eval-gate` and `eval-gate-v2` green before merging.

## Lab and Agent Constraints

Follow `README.md`, `CHECKPOINTS.md`, `RUBRIC.md`, and `SUBMISSION.md`. Never hand-edit reports, inline labels, weaken thresholds, or alter supplied variants/traps/tests to pass. Keep baselines tied to their eval-set version.

Obtain approval for new work groups; proceed within existing authorization. The owner handles Git publication unless explicitly delegated. Record assistant work, owner tasks, and reproduction steps clearly in `TIEN_DO_LAB.md`.
