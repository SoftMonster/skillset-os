"""Stop cleanly, with the reason, when these tests are run inside an installed split upload.

An upload may be one of several part skills, or may hold its largest groups as zips (see sync-skillset). The tests
read plain files from every group, so they only run in a working copy, where `skillset.py pull` has put the tree
back together."""
import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REASONS: list[str] = []
if (ROOT / "PARTS.json").is_file():
    _spec = importlib.util.spec_from_file_location("_skillset_parts", ROOT / "scripts" / "skillset.py")
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules[_spec.name] = _mod          # dataclasses look their module up here
    _spec.loader.exec_module(_mod)
    REASONS, _ = _mod.verify_parts(ROOT)
    REASONS.append("tests run only in a working copy: `python3 scripts/skillset.py pull` merges every part into one tree")
if (ROOT / "PACKED.json").is_file():
    REASONS.append("this upload holds zipped groups; tests run only in a working copy: "
                   "`python3 scripts/skillset.py pull` unpacks them")
collect_ignore_glob = ["test_*.py"] if REASONS else []


def pytest_report_header(config):
    return [f"NOT RUN: {reason}" for reason in REASONS]


def pytest_terminal_summary(terminalreporter):
    for reason in REASONS:
        terminalreporter.write_line(f"NOT RUN: {reason}")
