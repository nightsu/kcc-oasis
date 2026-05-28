from __future__ import annotations

from pathlib import Path


def requirements_file(project_root: Path, *, full_mode: bool) -> Path:
    if full_mode:
        return project_root / "vendor" / "kcc" / "requirements.txt"
    return project_root / "requirements-cli.txt"
