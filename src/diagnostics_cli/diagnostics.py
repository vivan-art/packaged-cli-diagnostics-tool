from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


DEVELOPER_TOOLS = ("git", "pip", "python", "pytest")

SAFE_ENV_VARS = (
    "PATH",
    "PYTHONPATH",
    "VIRTUAL_ENV",
    "HOME",
    "USERPROFILE",
)


def python_info() -> Dict[str, object]:
    return {
        "name": "python",
        "version": sys.version.split()[0],
        "executable": sys.executable,
        "status": "ok",
    }


def disk_info(path: str = ".") -> Dict[str, object]:
    target = Path(path)

    if not target.exists() or not target.is_dir():
        return {
            "name": "disk",
            "path": str(target),
            "status": "error",
            "error": "path does not exist or is not a directory",
        }

    usage = shutil.disk_usage(str(target))

    return {
        "name": "disk",
        "path": str(target.resolve()),
        "total_bytes": usage.total,
        "used_bytes": usage.used,
        "free_bytes": usage.free,
        "free_percent": round(
            (usage.free / usage.total) * 100, 2
        ) if usage.total else 0,
        "status": "ok",
    }


def environment_info() -> Dict[str, object]:
    variables = {}

    for key in SAFE_ENV_VARS:
        if key in os.environ:
            variables[key] = os.environ[key]

    return {
        "name": "environment",
        "variables": variables,
        "status": "ok",
        "note": "Only selected non-secret environment variables are reported.",
    }


def _tool_version(executable: str) -> Optional[str]:
    try:
        completed = subprocess.run(
            [executable, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )

        output = (
            completed.stdout or completed.stderr
        ).strip()

        return output or None

    except (OSError, subprocess.SubprocessError):
        return None


def developer_tools_info() -> List[Dict[str, object]]:
    results = []

    for tool in DEVELOPER_TOOLS:
        location = shutil.which(tool)

        results.append({
            "tool": tool,
            "installed": location is not None,
            "path": location,
            "version": _tool_version(tool) if location else None,
            "status": "ok" if location else "missing",
        })

    return results


def run_diagnostics(path: str = ".") -> Dict[str, object]:
    disk = disk_info(path)
    tools = developer_tools_info()

    return {
        "tool": "machine-diagnostics",
        "version": "1.0.0",
        "python": python_info(),
        "disk": disk,
        "environment": environment_info(),
        "developer_tools": tools,
        "overall_status": (
            "ok"
            if disk["status"] == "ok"
            and all(tool["installed"] for tool in tools)
            else "warning"
        ),
    }
