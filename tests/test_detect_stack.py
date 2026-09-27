"""Tests for software-dev/codebase-orientation/scripts/detect_stack.py."""
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "subskills/software-dev/subskills/codebase-orientation/scripts/detect_stack.py"
spec = importlib.util.spec_from_file_location("detect_stack", SCRIPT)
ds = importlib.util.module_from_spec(spec)
sys.modules["detect_stack"] = ds
spec.loader.exec_module(ds)


def test_node_project_uses_lockfile_manager_and_scripts(tmp_path):
    (tmp_path / "package.json").write_text(json.dumps({
        "scripts": {"test": "vitest", "lint": "eslint .", "build:prod": "vite build"},
        "devDependencies": {"vitest": "1", "typescript": "5"}, "dependencies": {"react": "18"},
    }))
    (tmp_path / "pnpm-lock.yaml").write_text("")
    (tmp_path / "src").mkdir()
    (tmp_path / "src/app.tsx").write_text("")
    (tmp_path / "node_modules/x").mkdir(parents=True)
    (tmp_path / "node_modules/x/ignored.js").write_text("")
    r = ds.detect(tmp_path)
    assert r["package_managers"] == ["pnpm"]
    assert r["commands"]["test"] == ["pnpm test"]
    assert r["commands"]["build"] == ["pnpm build:prod"]
    assert {"React", "Vitest", "TypeScript"} <= set(r["frameworks"])
    assert "JavaScript" not in r["languages"]  # node_modules skipped


def test_python_and_make_targets(tmp_path):
    (tmp_path / "pyproject.toml").write_text('[project]\ndependencies=["fastapi"]\n[dependency-groups]\ndev=["pytest","ruff"]\n')
    (tmp_path / "uv.lock").write_text("")
    (tmp_path / "Makefile").write_text("test:\n\tpytest\nfmt:\n\truff format\nVAR:=1\n")
    (tmp_path / "app.py").write_text("")
    r = ds.detect(tmp_path)
    assert "uv" in r["package_managers"]
    assert "uv run pytest" in r["commands"]["test"]
    assert "make test" in r["commands"]["test"]
    assert "make fmt" in r["commands"]["format"]
    assert "FastAPI" in r["frameworks"]


def test_missing_dir_exits_2(tmp_path, capsys):
    assert ds.main([str(tmp_path / "nope")]) == 2
    assert "not a directory" in capsys.readouterr().err
