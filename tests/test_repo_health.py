"""Repository health checks run in CI (and locally with `pytest`)."""
import ast
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".github", "node_modules", "venv", ".venv", "__pycache__"}


def _files(suffix):
    return [p for p in ROOT.rglob(f"*{suffix}") if not SKIP_DIRS & set(p.parts)]


def test_readme_has_core_sections():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    for heading in ("Overview", "How to Run"):
        assert heading in text, f"README is missing a '{heading}' section"


def test_python_files_parse():
    for path in _files(".py"):
        ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def test_notebooks_are_valid_json_with_cells():
    for path in _files(".ipynb"):
        nb = json.loads(path.read_text(encoding="utf-8"))
        assert "cells" in nb, f"{path.name} has no cells"


def test_no_student_ids_committed():
    pattern = re.compile(r"\b27\d{8}\b")
    for path in list(_files(".py")) + list(_files(".md")) + list(_files(".ipynb")):
        assert not pattern.search(path.read_text(encoding="utf-8", errors="ignore")), f"student ID found in {path.name}"
