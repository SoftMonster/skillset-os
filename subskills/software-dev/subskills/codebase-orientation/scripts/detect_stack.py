#!/usr/bin/env python3
"""Detect a repository's languages, tooling and the commands to build, test, lint and run it.

Usage:
    python3 detect_stack.py [REPO_DIR] [--json]

Prints a short report (or JSON with --json): languages by file count, package managers,
frameworks, test/lint/format/typecheck/build commands inferred from manifests, CI systems,
containers, and likely entry points. It only reads files; it never runs project code.

Exit codes: 0 success, 2 REPO_DIR missing or not a directory.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "env", "__pycache__", "dist", "build", "target",
             ".next", ".nuxt", "vendor", ".tox", ".mypy_cache", ".pytest_cache", "coverage", ".idea", ".gradle"}
EXT_LANG = {
    ".py": "Python", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript", ".jsx": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".go": "Go", ".rs": "Rust", ".java": "Java", ".kt": "Kotlin",
    ".rb": "Ruby", ".php": "PHP", ".cs": "C#", ".cpp": "C++", ".cc": "C++", ".c": "C", ".h": "C/C++ header",
    ".swift": "Swift", ".scala": "Scala", ".ex": "Elixir", ".exs": "Elixir", ".dart": "Dart", ".sql": "SQL",
    ".sh": "Shell", ".vue": "Vue", ".svelte": "Svelte", ".tf": "Terraform",
}
# Walking huge monorepos fully is slow and adds nothing to the proportions; stop after this many files.
MAX_FILES = 50_000


def walk(root: Path):
    count = 0
    stack = [root]
    while stack:
        d = stack.pop()
        try:
            entries = list(d.iterdir())
        except OSError:
            continue
        for p in entries:
            if p.is_dir():
                if p.name not in SKIP_DIRS and not p.is_symlink():
                    stack.append(p)
            else:
                count += 1
                if count > MAX_FILES:
                    return
                yield p


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def detect(root: Path) -> dict:
    langs: Counter = Counter()
    names: set[str] = set()
    rel_files: list[str] = []
    for p in walk(root):
        rel = p.relative_to(root).as_posix()
        rel_files.append(rel)
        names.add(p.name)
        lang = EXT_LANG.get(p.suffix.lower())
        if lang:
            langs[lang] += 1

    top = {p.name for p in root.iterdir()}
    r: dict = {"root": str(root), "languages": dict(langs.most_common()), "package_managers": [],
               "frameworks": [], "commands": {}, "ci": [], "containers": [], "entry_points": [], "notes": []}
    cmds = r["commands"]

    def add(kind: str, cmd: str):
        cmds.setdefault(kind, [])
        if cmd not in cmds[kind]:
            cmds[kind].append(cmd)

    # JavaScript / TypeScript
    pkg = root / "package.json"
    if pkg.exists():
        pm = "pnpm" if "pnpm-lock.yaml" in top else "yarn" if "yarn.lock" in top else \
             "bun" if ("bun.lockb" in top or "bun.lock" in top) else "npm"
        r["package_managers"].append(pm)
        try:
            data = json.loads(read(pkg) or "{}")
        except json.JSONDecodeError:
            data = {}
            r["notes"].append("package.json is not valid JSON")
        run = "npm run" if pm == "npm" else pm
        for name in (data.get("scripts") or {}):
            low = name.lower()
            for kind in ("test", "lint", "build", "dev", "start", "typecheck", "format"):
                if low == kind or low.startswith(kind + ":"):
                    add(kind, f"{run} {name}")
        deps = {**(data.get("dependencies") or {}), **(data.get("devDependencies") or {})}
        for dep, fw in (("next", "Next.js"), ("react", "React"), ("vue", "Vue"), ("svelte", "Svelte"),
                        ("@angular/core", "Angular"), ("express", "Express"), ("fastify", "Fastify"),
                        ("@nestjs/core", "NestJS"), ("vitest", "Vitest"), ("jest", "Jest"),
                        ("@playwright/test", "Playwright"), ("prisma", "Prisma"), ("typescript", "TypeScript")):
            if dep in deps:
                r["frameworks"].append(fw)
        for key in ("main", "bin", "module"):
            if isinstance(data.get(key), str):
                r["entry_points"].append(data[key])

    # Python
    pyproject = read(root / "pyproject.toml") if "pyproject.toml" in top else ""
    if pyproject or "requirements.txt" in top or "setup.py" in top:
        pm = "uv" if "uv.lock" in top else "poetry" if "poetry.lock" in top else "pip"
        r["package_managers"].append(pm)
        req = pyproject + read(root / "requirements.txt") + read(root / "requirements-dev.txt")
        prefix = "uv run " if pm == "uv" else "poetry run " if pm == "poetry" else ""
        if "pytest" in req or "conftest.py" in names or any(f.startswith("tests/") for f in rel_files):
            add("test", f"{prefix}pytest")
        if "ruff" in req:
            add("lint", f"{prefix}ruff check .")
            add("format", f"{prefix}ruff format .")
        if "black" in req:
            add("format", f"{prefix}black .")
        if "mypy" in req:
            add("typecheck", f"{prefix}mypy .")
        if "pyright" in req:
            add("typecheck", f"{prefix}pyright")
        for dep, fw in (("django", "Django"), ("fastapi", "FastAPI"), ("flask", "Flask"),
                        ("sqlalchemy", "SQLAlchemy"), ("pydantic", "Pydantic")):
            if re.search(rf"(?i)\b{dep}\b", req):
                r["frameworks"].append(fw)
        if "manage.py" in top:
            r["entry_points"].append("manage.py")
    if "tox.ini" in top:
        add("test", "tox")

    # Other ecosystems
    if "go.mod" in top:
        r["package_managers"].append("go modules")
        add("test", "go test ./...")
        add("build", "go build ./...")
        add("lint", "go vet ./...")
        r["entry_points"] += [f for f in rel_files if f.endswith("main.go")][:5]
    if "Cargo.toml" in top:
        r["package_managers"].append("cargo")
        add("test", "cargo test")
        add("build", "cargo build")
        add("lint", "cargo clippy --all-targets")
        add("format", "cargo fmt")
    if "pom.xml" in top:
        r["package_managers"].append("maven")
        add("test", "./mvnw test" if "mvnw" in top else "mvn test")
        add("build", "./mvnw package" if "mvnw" in top else "mvn package")
    if top & {"build.gradle", "build.gradle.kts"}:
        r["package_managers"].append("gradle")
        g = "./gradlew" if "gradlew" in top else "gradle"
        add("test", f"{g} test")
        add("build", f"{g} build")
    if "Gemfile" in top:
        r["package_managers"].append("bundler")
        add("test", "bundle exec rspec" if "spec" in top else "bundle exec rake test")
        if "rails" in read(root / "Gemfile"):
            r["frameworks"].append("Rails")
    if "composer.json" in top:
        r["package_managers"].append("composer")
        add("test", "vendor/bin/phpunit")
    if any(f.endswith((".csproj", ".sln")) for f in rel_files):
        r["package_managers"].append("dotnet")
        add("test", "dotnet test")
        add("build", "dotnet build")

    # Makefile / justfile targets are usually the canonical commands, so list them too.
    for mk, tool in (("Makefile", "make"), ("justfile", "just")):
        if mk in top:
            for target in re.findall(r"(?m)^([a-zA-Z][\w-]*):(?!=)", read(root / mk)):
                if target.lower() in ("test", "lint", "build", "run", "dev", "check", "format", "fmt", "typecheck"):
                    kind = {"fmt": "format", "check": "lint", "run": "start"}.get(target.lower(), target.lower())
                    add(kind, f"{tool} {target}")

    # CI and containers
    if any(f.startswith(".github/workflows/") for f in rel_files):
        r["ci"].append("GitHub Actions")
    if ".gitlab-ci.yml" in top:
        r["ci"].append("GitLab CI")
    if ".circleci" in top:
        r["ci"].append("CircleCI")
    if "Jenkinsfile" in top:
        r["ci"].append("Jenkins")
    r["containers"] = sorted(f for f in rel_files if Path(f).name in
                             ("Dockerfile", "docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml"))[:10]
    if ".pre-commit-config.yaml" in top:
        r["notes"].append("pre-commit hooks configured: run `pre-commit run --all-files` before committing")
    if not langs:
        r["notes"].append("no source files recognised; check REPO_DIR")
    r["frameworks"] = sorted(set(r["frameworks"]))
    r["file_count"] = len(rel_files)
    return r


def render(r: dict) -> str:
    total = sum(r["languages"].values()) or 1
    out = [f"Repository: {r['root']} ({r['file_count']} files scanned)"]
    langs = ", ".join(f"{k} {v * 100 // total}%" for k, v in list(r["languages"].items())[:6])
    out.append(f"Languages: {langs or 'none detected'}")
    for label, key in (("Package managers", "package_managers"), ("Frameworks/tools", "frameworks"),
                       ("CI", "ci"), ("Containers", "containers"), ("Entry points", "entry_points")):
        if r[key]:
            out.append(f"{label}: {', '.join(r[key])}")
    if r["commands"]:
        out.append("Commands:")
        for kind in ("build", "test", "lint", "format", "typecheck", "dev", "start"):
            if kind in r["commands"]:
                out.append(f"  {kind:<9} {' | '.join(r['commands'][kind])}")
    else:
        out.append("Commands: none inferred; read the README and CI config")
    out += [f"Note: {n}" for n in r["notes"]]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("repo", nargs="?", default=".", help="repository folder (default: current folder)")
    ap.add_argument("--json", action="store_true", help="print JSON instead of a report")
    args = ap.parse_args(argv)
    root = Path(args.repo).resolve()
    if not root.is_dir():
        print(f"error: {root} is not a directory; pass the repository folder (unzip an uploaded repo first)",
              file=sys.stderr)
        return 2
    r = detect(root)
    print(json.dumps(r, indent=2) if args.json else render(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
