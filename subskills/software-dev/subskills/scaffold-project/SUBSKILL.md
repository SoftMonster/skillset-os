---
name: scaffold-project
description: "Creates a new project skeleton with a sensible layout, dependency manifest, formatter, linter, type checking, a test runner with one passing test, a README, gitignore and a CI workflow, using current conventions for the chosen stack. Use when the user asks to start, bootstrap, scaffold, set up or initialise a new app, service, library, CLI or monorepo, or asks what structure and tooling a new project should have."
trigger: "start or scaffold a new project, service, library or CLI"
metadata:
  version: "1.1.0"
---

# Scaffold a project

🧬 **Core meme:** Start with a skeleton that builds, lints and passes one test.

Create a new project that is boring in the best way: standard layout, pinned modern tooling, a passing test, CI on day one, and a README that gets a newcomer running in under five minutes. Prefer the ecosystem's official generator when one exists, then add what it leaves out.

## Workflow

```
- [ ] 1. Settle the stack
- [ ] 2. Generate or write the skeleton
- [ ] 3. Add quality tooling
- [ ] 4. Add CI, README, gitignore, licence
- [ ] 5. Prove it works
- [ ] 6. Deliver
```

1. **Stack.** Use what the person named. If they did not, pick the default below for the kind of project and say so in one line rather than asking.
2. **Skeleton.** Use the official generator where it exists (`npm create vite@latest`, `cargo new`, `uv init`, `go mod init`, `dotnet new`), because it tracks current conventions better than a hand-written layout. Otherwise write the layout by hand.
3. **Quality tooling.** Formatter, linter, type checker and test runner, each wired to one command. Pin versions in the lockfile.
4. **Supporting files.** A `.gitignore` for the language, a README (what, quick start, commands, layout), a `LICENSE` only if the person names one, `.env.example` rather than `.env` if configuration is needed, and a CI workflow (see `ci-cd-pipeline`) that runs lint, type check and test.
5. **Prove it.** Install, then run lint, type check and tests in the sandbox and make sure they pass. A scaffold that fails its own checks costs the person their first hour.
6. **Deliver.** Zip the project (exclude `node_modules`, `.venv`, `target`) and present it, or present the files if there are only a few. List the commands to run first.

## Defaults by project kind

| Kind | Default stack |
|---|---|
| Python library or CLI | `uv`, `src/` layout, `pyproject.toml`, ruff (lint + format), mypy or pyright, pytest, Typer for CLIs |
| Python web API | above + FastAPI, Pydantic settings, uvicorn |
| TypeScript web app | Vite + React + TypeScript (strict), ESLint, Prettier, Vitest, Playwright for e2e if asked |
| Node service | TypeScript (strict), Fastify, tsx for dev, Vitest, ESLint, Prettier |
| Go service or CLI | `cmd/<name>/main.go`, `internal/`, `go vet` + staticcheck, `go test`, Cobra for CLIs |
| Rust | `cargo new`, clippy, rustfmt, clap for CLIs |

## Example: Python CLI layout

```
mytool/
├── pyproject.toml          # project metadata, deps, ruff/mypy/pytest config in one place
├── src/mytool/__init__.py
├── src/mytool/cli.py       # Typer app; entry point declared in [project.scripts]
├── tests/test_cli.py       # one real test using typer.testing.CliRunner
├── .github/workflows/ci.yml
├── .gitignore
└── README.md
```

## Gotchas

- Generators prompt interactively. Pass flags or templates non-interactively (`npm create vite@latest app -- --template react-ts`), or the command hangs.
- The sandbox reaches npm and PyPI but not every registry. If a generator downloads templates from elsewhere, write the files by hand.
- Do not commit secrets, `.env` files or lockfiles for libraries whose ecosystem says not to. Do commit lockfiles for applications.
- Keep the scaffold minimal. Every extra library is a decision the person did not make.

## Commands

- 🏗️ **A skeleton that builds, lints and passes** · `scaffold project`: Starts a new project, service, library or CLI: picks the stack, lays out a skeleton with quality tooling and supporting files, proves it builds and one test passes, and delivers it.
  - 🧰 `choose stack`: Picks language, framework and tooling from the project kind and the person's constraints, with defaults by kind.
  - 📁 `create skeleton`: Lays out folders, entry point, config and one passing test.
  - 🧹 `add quality-tooling`: Adds formatter, linter, type checker, test runner and a CI workflow.
  - 📄 `add project-files`: Adds README, licence, .gitignore and contribution notes.
  - ✅ `prove skeleton`: Runs install, lint and tests in the sandbox and shows they pass before delivery.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/scaffold-project` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/scaffold-project` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
