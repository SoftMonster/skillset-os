---
name: ci-cd-pipeline
description: "Builds and fixes build and delivery automation: GitHub Actions and other CI workflows, Dockerfiles and compose files, caching, test matrices, release and deploy jobs, and secret handling. Use when the user asks to set up, write or debug CI, CD, a pipeline, GitHub Actions, GitLab CI, a Dockerfile, container build, deployment or release automation, or a failing build. Do not use for a failing test whose cause is in the code; use debug-issue."
trigger: "set up or fix CI/CD, GitHub Actions, Docker or deployment"
command: "automate pipeline"
metadata:
  version: "1.0.1"
---

# CI/CD pipeline

🧬 **Core meme:** Automate build, test and release so every change is checked the same way.

Build pipelines that are fast, deterministic and safe: every push is linted, type-checked and tested; releases are reproducible; secrets and permissions are minimal. Default to GitHub Actions unless the repository already uses something else.

## Workflow

```
- [ ] 1. Find the real commands
- [ ] 2. Write the workflow
- [ ] 3. Containerise if needed
- [ ] 4. Add release or deploy
- [ ] 5. Validate
```

1. **Commands.** Take the build, lint and test commands from the project (run `codebase-orientation`'s `detect_stack.py`, or read the Makefile). CI should run the same commands developers run locally.
2. **Workflow.** Start from the template below. Add a version matrix only for libraries that support several runtimes; applications test on the version they deploy.
3. **Container.** Use a multi-stage Dockerfile: build in a full image, run in a slim or distroless one, as a non-root user, with dependency layers copied before source for caching, and a `.dockerignore`.
4. **Release or deploy.** Trigger on tags (`v*`) or on merges to `main`. Use OIDC federation to the cloud (no long-lived keys), environments with required reviewers for production, and a documented rollback.
5. **Validate.** Lint workflows with `actionlint` (`go install github.com/rhysd/actionlint/cmd/actionlint@latest`, or its release binary) and Dockerfiles with `hadolint`. Build the Docker image in the sandbox if Docker is available; otherwise say it was not built.

## Template: GitHub Actions CI

```yaml
name: CI
on:
  push: {branches: [main]}
  pull_request:
permissions:
  contents: read                     # least privilege; widen per job only if needed
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true           # stop superseded runs on the same branch
jobs:
  check:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v5  # or actions/setup-node@v4 with cache: npm, etc.
        with: {enable-cache: true}
      - run: uv sync --frozen
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy .
      - run: uv run pytest -q
```

## Template: Python Dockerfile

```dockerfile
FROM python:3.12-slim AS build
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY src ./src
RUN uv sync --frozen --no-dev

FROM python:3.12-slim
WORKDIR /app
RUN useradd --create-home app
COPY --from=build /app /app
USER app
ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "myapp"]
```

## Debugging a failing build

1. Read the first error in the log, not the last. Later errors are usually consequences.
2. Classify it: code (tests fail locally too, so use `debug-issue`), environment (versions, missing system packages, env vars), flaky (passes on re-run: find the cause, do not just add retries), or infrastructure (rate limits, runner disk space, expired secrets).
3. Reproduce locally with the same versions, or in the same container image.

## Gotchas

- Third-party actions run with your token. Pin them to a full commit SHA in security-sensitive repositories, and never give `pull_request_target` workflows write access to untrusted code.
- Secrets are not available to PRs from forks. Design jobs that need them to run after merge.
- Caches keyed only on branch go stale; key on the lockfile hash.
- `latest` tags in images and tools make builds unreproducible. Pin versions for anything that ships.

<!-- folder:start -->
## This folder

Asked what this folder holds, or to review it, look before answering. `python3 <top>/scripts/skillset.py contents software-dev/ci-cd-pipeline` lists every file in it with a line on what each is, and `python3 <top>/scripts/skillset.py review software-dev/ci-cd-pipeline` audits them for problems. Then read the files the question needs, check them for clarity, accuracy, contradictions and anything out of date, and answer from them.
<!-- folder:end -->
