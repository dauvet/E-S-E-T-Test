#!/usr/bin/env python3
"""
Run Account and Key Generator locally without GitHub Actions.

Usage:
  python run_account_and_key_generator.py --account 3 --key 1 --mail emailfake --key-type --key
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import List

import venv


ROOT = Path(__file__).resolve().parent
VENV_DIR = ROOT / ".venv_generator"
REQUIREMENTS = ROOT / "requirements.txt"
DEFAULT_ACCOUNT_COUNT = 1
DEFAULT_KEY_COUNT = 1
DEFAULT_MAIL = "emailfake"
DEFAULT_KEY_TYPE = "--key"

MAIL_PROVIDERS = [
    "1secmail",
    "guerrillamail",
    "developermail",
    "mailticking",
    "fakemail",
    "inboxes",
    "incognitomail",
    "emailfake",
]

KEY_TYPES = ("--key", "--small-business-key")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Local runner for Account and Key Generator workflow."
    )
    parser.add_argument(
        "--account",
        type=int,
        default=DEFAULT_ACCOUNT_COUNT,
        help="Number of accounts to generate (default: 0).",
    )
    parser.add_argument(
        "--key",
        type=int,
        default=DEFAULT_KEY_COUNT,
        help="Number of keys to generate (default: 1).",
    )
    parser.add_argument(
        "--mail",
        choices=MAIL_PROVIDERS,
        default=DEFAULT_MAIL,
        help="Mail provider used for generation.",
    )
    parser.add_argument(
        "--key-type",
        choices=KEY_TYPES,
        default=DEFAULT_KEY_TYPE,
        help="Key generation mode.",
    )
    parser.add_argument(
        "--use-system-python",
        action="store_true",
        help="Use current Python instead of auto-created local virtual environment.",
    )
    return parser.parse_args()


def make_venv(python: Path) -> Path:
    if python.exists():
        return python

    print("Creating local virtual environment: .venv_generator")
    venv.EnvBuilder(with_pip=True).create(VENV_DIR)
    return python


def get_executables() -> tuple[Path, Path]:
    if os.name == "nt":
        py = VENV_DIR / "Scripts" / "python.exe"
        pip = VENV_DIR / "Scripts" / "pip.exe"
    else:
        py = VENV_DIR / "bin" / "python"
        pip = VENV_DIR / "bin" / "pip"
    return py, pip


def ensure_python(env: argparse.Namespace) -> str:
    if env.use_system_python:
        return sys.executable

    VENV_DIR.mkdir(exist_ok=True)
    py, pip = get_executables()
    py = make_venv(py)
    if not REQUIREMENTS.exists():
        raise FileNotFoundError(f"Không thấy file requirements.txt tại {REQUIREMENTS}")

    print("Installing dependencies into local venv...")
    subprocess.run([str(pip), "install", "-r", str(REQUIREMENTS)], check=True)
    return str(py)


def run_main(python_exe: str, args: argparse.Namespace) -> None:
    base_cmd: List[str] = [
        python_exe,
        str(ROOT / "main.py"),
        "--auto-detect-browser",
        "--skip-update-check",
        "--no-logo",
        "--disable-progress-bar",
        "--disable-logging",
    ]

    if args.account > 0:
        account_cmd = base_cmd + [
            "--account",
            "--email-api",
            args.mail,
            "--repeat",
            str(args.account),
        ]
        print(f"Running account generator: {args.account}")
        subprocess.run(account_cmd, check=True, cwd=str(ROOT))

    if args.key > 0:
        key_cmd = base_cmd + [
            args.key_type,
            "--email-api",
            args.mail,
            "--repeat",
            str(args.key),
        ]
        print(f"Running key generator: {args.key} with {args.key_type}")
        subprocess.run(key_cmd, check=True, cwd=str(ROOT))


def print_outputs() -> None:
    accounts = sorted(ROOT.glob("*ACCOUNTS*.txt"))
    keys = sorted(ROOT.glob("*KEYS*.txt"))

    print("\n--- Account files ---")
    if accounts:
        for path in accounts:
            print(f"- {path.name}")
    else:
        print("No account file matched: *ACCOUNTS*.txt")

    print("\n--- Key files ---")
    if keys:
        for path in keys:
            print(f"- {path.name}")
    else:
        print("No key file matched: *KEYS*.txt")


def main() -> None:
    args = parse_args()

    if args.account == 0 and args.key == 0:
        print("Nothing to run: both --account and --key are set to 0.")
        return

    python_exe = ensure_python(args)
    run_main(python_exe, args)
    print_outputs()


if __name__ == "__main__":
    main()
