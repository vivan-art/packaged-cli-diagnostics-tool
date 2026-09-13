from __future__ import annotations

import argparse
import json

from .diagnostics import run_diagnostics


def build_parser():
    parser = argparse.ArgumentParser(
        prog="machine-diagnostics",
        description="Inspect Python, disk space, environment, and developer tools.",
    )

    parser.add_argument(
        "--path",
        default=".",
        help="Directory whose filesystem is inspected.",
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Print structured JSON output.",
    )

    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 1 when diagnostics are not fully successful.",
    )

    return parser


def human_report(data):
    lines = [
        "MACHINE DIAGNOSTICS REPORT",
        "==========================",
        f"Overall status: {data['overall_status']}",
        "",
        "Python",
        f"  Version: {data['python']['version']}",
        f"  Executable: {data['python']['executable']}",
        "",
        "Disk",
        f"  Path: {data['disk']['path']}",
        f"  Free: {data['disk'].get('free_percent', 0)}%",
        f"  Status: {data['disk']['status']}",
        "",
        "Environment",
        f"  Reported variables: "
        f"{len(data['environment']['variables'])}",
        "",
        "Developer tools",
    ]

    for tool in data["developer_tools"]:
        version = tool["version"] or "not found"
        lines.append(f"  {tool['tool']}: {version}")

    return "\n".join(lines)


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    data = run_diagnostics(args.path)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(human_report(data))

    if args.strict and data["overall_status"] != "ok":
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
