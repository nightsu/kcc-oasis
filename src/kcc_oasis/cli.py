from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Iterable


PROFILE_ALIASES = {
    "oasis": "KO",
    "ko": "KO",
    "paperwhite": "KPW",
    "kpw": "KPW",
    "paperwhite34": "KPW34",
    "paperwhite3": "KPW34",
    "paperwhite4": "KPW34",
    "kpw34": "KPW34",
    "paperwhite5": "KPW5",
    "signature": "KPW5",
    "kpw5": "KPW5",
    "paperwhite6": "KPW6",
    "kpw6": "KPW6",
}

KCC_PROFILES = {"KO", "KPW", "KPW34", "KPW5", "KPW6"}
KCC_FORMATS = {"EPUB", "MOBI", "CBZ", "PDF", "KFX", "MOBI+EPUB", "AUTO"}


def resolve_profile(profile: str) -> str:
    value = profile.strip()
    alias = PROFILE_ALIASES.get(value.lower())
    if alias:
        return alias
    upper_value = value.upper()
    if upper_value in KCC_PROFILES:
        return upper_value
    raise ValueError(
        f"Unsupported profile '{profile}'. Use one of: oasis, paperwhite, "
        "paperwhite34, paperwhite5, paperwhite6, KO, KPW, KPW34, KPW5, KPW6."
    )


def normalize_format(output_format: str) -> str:
    value = output_format.strip().upper()
    if value in KCC_FORMATS:
        return value
    raise ValueError(
        f"Unsupported format '{output_format}'. Use one of: EPUB, MOBI, CBZ, PDF, KFX, MOBI+EPUB, Auto."
    )


def build_kcc_command(
    *,
    python_bin: Path,
    kcc_script: Path,
    inputs: Iterable[Path],
    profile: str,
    output: Path | None,
    output_format: str,
    manga: bool,
    hq: bool,
    passthrough: list[str],
) -> list[str]:
    resolved_format = normalize_format(output_format)
    command = [
        str(python_bin),
        str(kcc_script),
        "-p",
        resolve_profile(profile),
        "-f",
        resolved_format,
    ]

    if resolved_format == "EPUB":
        command.append("--nokepub")
    if manga:
        command.append("-m")
    if hq:
        command.append("-q")
    if output is not None:
        command.extend(["-o", str(output)])

    command.extend(passthrough)
    command.extend(str(path) for path in inputs)
    return command


def main(argv: list[str] | None = None) -> int:
    wrapper_args, passthrough = _split_passthrough(sys.argv[1:] if argv is None else argv)
    args = _parser().parse_args(wrapper_args)

    if args.list_profiles:
        print_profiles()
        return 0

    if not args.inputs:
        _parser().error("at least one comic folder, archive, or PDF input is required")

    project_root = Path(__file__).resolve().parents[2]
    python_bin = project_root / ".venv" / "bin" / "python"
    kcc_script = project_root / "vendor" / "kcc" / "kcc-c2e.py"

    if not python_bin.exists():
        print(f"Missing Python environment: {python_bin}", file=sys.stderr)
        print("Run scripts/bootstrap.sh from the kcc-oasis project root.", file=sys.stderr)
        return 2
    if not kcc_script.exists():
        print(f"Missing vendored KCC script: {kcc_script}", file=sys.stderr)
        return 2

    try:
        command = build_kcc_command(
            python_bin=python_bin,
            kcc_script=kcc_script,
            inputs=[Path(path).expanduser() for path in args.inputs],
            profile=args.profile,
            output=Path(args.output).expanduser() if args.output else None,
            output_format=args.output_format,
            manga=not args.no_manga,
            hq=args.hq,
            passthrough=passthrough,
        )
    except ValueError as error:
        print(error, file=sys.stderr)
        return 2

    if args.dry_run:
        print(" ".join(_quote(part) for part in command))
        return 0

    env = os.environ.copy()
    vendor_path = str(kcc_script.parent)
    env["PYTHONPATH"] = vendor_path + os.pathsep + env.get("PYTHONPATH", "")
    completed = subprocess.run(command, env=env, check=False)
    return completed.returncode


def print_profiles() -> None:
    print("oasis        KO     Kindle Oasis 2/3")
    print("paperwhite   KPW    Kindle Paperwhite 1/2")
    print("paperwhite34 KPW34  Kindle Paperwhite 3/4")
    print("paperwhite5  KPW5   Kindle Paperwhite 5/Signature Edition")
    print("paperwhite6  KPW6   Kindle Paperwhite 6")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kcc-oasis",
        description="A small standalone CLI wrapper around KCC, defaulting to Kindle Oasis EPUB output.",
    )
    parser.add_argument("inputs", nargs="*", help="Comic folder, CBZ/ZIP/CBR/RAR/7Z archive, or PDF.")
    parser.add_argument(
        "-p",
        "--profile",
        default="oasis",
        help="Friendly profile or KCC profile code. Default: oasis.",
    )
    parser.add_argument(
        "-f",
        "--format",
        dest="output_format",
        default="EPUB",
        help="Output format passed to KCC. Default: EPUB. Use MOBI for Kindle USB workflows.",
    )
    parser.add_argument("-o", "--output", help="Output directory or file path passed to KCC.")
    parser.add_argument("--no-manga", action="store_true", help="Disable right-to-left manga mode.")
    parser.add_argument("-q", "--hq", action="store_true", help="Enable KCC high-quality magnification mode.")
    parser.add_argument("--dry-run", action="store_true", help="Print the underlying KCC command without running it.")
    parser.add_argument("--list-profiles", action="store_true", help="List supported friendly profiles.")
    return parser


def _split_passthrough(arguments: list[str]) -> tuple[list[str], list[str]]:
    if "--" not in arguments:
        return arguments, []
    separator = arguments.index("--")
    return arguments[:separator], arguments[separator + 1 :]


def _quote(value: str) -> str:
    if not value or any(char.isspace() for char in value):
        return "'" + value.replace("'", "'\"'\"'") + "'"
    return value


if __name__ == "__main__":
    raise SystemExit(main())
