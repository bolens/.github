#!/usr/bin/env python3
"""Run selected correctness linters against tracked, maintained repository files."""
import argparse
import fnmatch
import json
import os
from pathlib import Path
import subprocess

KINDS = {"python", "shell", "javascript", "css", "markdown"}
SUFFIXES = {"python": {".py"}, "shell": {".sh"}, "javascript": {".js", ".mjs", ".cjs"}, "css": {".css"}, "markdown": {".md"}}


def select(root, config):
    if set(config) - (KINDS | {"exclude", "notes"}):
        raise ValueError("Unknown source-lint configuration key")
    for key in KINDS | {"exclude"}:
        if key in config and (not isinstance(config[key], list) or not all(isinstance(x, str) and x for x in config[key])):
            raise ValueError(f"{key} must be a list of nonempty glob strings")
    environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=root, env=environment)
    files = [Path(x.decode()) for x in raw.split(b"\0") if x]
    result = {}
    for kind in sorted(KINDS & config.keys()):
        selected = []
        for file in files:
            name = file.as_posix()
            if name.startswith((".specify/", ".agents/")) or any(fnmatch.fnmatchcase(name, pattern) for pattern in config.get("exclude", [])):
                continue
            if not any(fnmatch.fnmatchcase(name, pattern) for pattern in config[kind]):
                continue
            path = root / file
            if path.is_symlink() or not path.resolve().is_relative_to(root.resolve()):
                raise ValueError(f"Refusing symlink source: {name}")
            suffix_matches = file.suffix in SUFFIXES[kind]
            if kind == "shell" and not suffix_matches and path.is_file():
                first = path.read_bytes().split(b"\n", 1)[0]
                suffix_matches = first.startswith(b"#!") and first.split()[-1:] in ([b"bash"], [b"sh"], [b"/bin/bash"], [b"/bin/sh"])
            if suffix_matches:
                selected.append(name)
        if not selected:
            raise ValueError(f"Configured {kind} check matched no tracked files")
        result[kind] = selected
    if not result:
        raise ValueError("No language checks configured")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    config = json.loads((root / ".github/source-lint.json").read_text())
    selected = select(root, config)
    if args.list:
        print(json.dumps(selected, indent=2))
        return
    driver = Path(__file__).resolve().parents[1] / "tools/source-lint/lint.mjs"
    failed = False
    for kind, files in selected.items():
        print(f"{kind}: checking {len(files)} tracked files", flush=True)
        if kind == "python":
            command = ["ruff", "check", "--isolated", "--select", "E9,F", "--"]
        elif kind == "shell":
            command = ["shellcheck", "--severity=warning", "--"]
        else:
            command = ["node", str(driver), kind]
        for start in range(0, len(files), 100):
            failed |= subprocess.run(command + files[start:start + 100], cwd=root, check=False).returncode != 0
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
