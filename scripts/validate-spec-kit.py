#!/usr/bin/env python3
"""Validate the repository-local GitHub Spec Kit installation."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

PLACEHOLDERS = ("[PROJECT_NAME]", "[VERSION]", "[RATIFICATION_DATE]",
                "[LAST_AMENDED_DATE]", "TODO")
METADATA_RE = re.compile(
    r"\*\*Version\*\*: (?P<version>\d+\.\d+\.\d+) \| "
    r"\*\*Ratified\*\*: (?P<ratified>\d{4}-\d{2}-\d{2}) \| "
    r"\*\*Last Amended\*\*: (?P<amended>\d{4}-\d{2}-\d{2})$",
    re.MULTILINE,
)


def load_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError(f"{path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path}: root must be an object")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate(root: Path, expected_version: str) -> list[str]:
    errors: list[str] = []
    integration_path = root / ".specify/integration.json"
    options_path = root / ".specify/init-options.json"
    constitution_path = root / ".specify/memory/constitution.md"
    try:
        integration = load_json(integration_path)
        options = load_json(options_path)
    except ValueError as exc:
        return [str(exc)]

    expected_integration = {
        "version": expected_version,
        "installed_integrations": ["codex"],
        "integration": "codex",
        "default_integration": "codex",
    }
    for key, expected in expected_integration.items():
        if integration.get(key) != expected:
            errors.append(f"{integration_path}: {key} is "
                          f"{integration.get(key)!r}; expected {expected!r}")

    settings = integration.get("integration_settings", {})
    if not isinstance(settings, dict):
        errors.append(f"{integration_path}: integration_settings must be an object")
        settings = {}
    settings = settings.get("codex", {})
    if not isinstance(settings, dict):
        errors.append(f"{integration_path}: Codex settings must be an object")
        settings = {}
    if settings.get("script") != "sh":
        errors.append(f"{integration_path}: Codex script integration must be sh")
    parsed_options = settings.get("parsed_options", {})
    if not isinstance(parsed_options, dict):
        errors.append(f"{integration_path}: parsed_options must be an object")
        parsed_options = {}
    if parsed_options.get("skills") is not True:
        errors.append(f"{integration_path}: Codex skills integration is disabled")

    expected_options = {
        "ai": "codex",
        "ai_skills": True,
        "feature_numbering": "sequential",
        "here": True,
        "integration": "codex",
        "script": "sh",
        "speckit_version": expected_version,
    }
    for key, expected in expected_options.items():
        if options.get(key) != expected:
            errors.append(f"{options_path}: {key} is {options.get(key)!r}; "
                          f"expected {expected!r}")

    manifests = sorted((root / ".specify/integrations").glob("*.manifest.json"))
    if {path.name for path in manifests} != {
        "codex.manifest.json", "speckit.manifest.json"
    }:
        errors.append("expected exactly the codex and speckit integration manifests")
    for manifest_path in manifests:
        try:
            manifest = load_json(manifest_path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if manifest.get("version") != expected_version:
            errors.append(f"{manifest_path}: version is "
                          f"{manifest.get('version')!r}; "
                          f"expected {expected_version!r}")
        files = manifest.get("files")
        if not isinstance(files, dict):
            errors.append(f"{manifest_path}: files must be an object")
            continue
        for relative, expected_hash in files.items():
            managed_path = root / relative
            parts = Path(relative).parts
            if (not parts or Path(relative).is_absolute() or ".." in parts
                    or any((root.joinpath(*parts[:index])).is_symlink()
                           for index in range(1, len(parts) + 1))):
                errors.append(f"{manifest_path}: unsafe managed path {relative}")
                continue
            if not managed_path.is_file():
                errors.append(f"{manifest_path}: missing managed file {relative}")
            elif sha256(managed_path) != expected_hash:
                errors.append(f"{manifest_path}: hash mismatch for {relative}")

    try:
        constitution = constitution_path.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append(f"{constitution_path}: {exc}")
    else:
        for placeholder in PLACEHOLDERS:
            if placeholder in constitution:
                errors.append(f"{constitution_path}: unresolved {placeholder}")
        if not METADATA_RE.search(constitution):
            errors.append(f"{constitution_path}: missing valid governance metadata")

    for script in sorted((root / ".specify/scripts/bash").glob("*.sh")):
        result = subprocess.run(["bash", "-n", str(script)], check=False,
                                capture_output=True, text=True)
        if result.returncode:
            errors.append(f"{script}: {result.stderr.strip()}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repositories", nargs="*", type=Path)
    parser.add_argument("--expected-version")
    args = parser.parse_args()
    repositories = args.repositories or [Path.cwd()]
    failed = False
    for repository in repositories:
        root = repository.resolve()
        expected_version = args.expected_version
        if not expected_version or expected_version == "current":
            try:
                expected_version = load_json(
                    root / ".specify/integration.json"
                ).get("version")
            except ValueError as exc:
                print(f"{root}: FAIL\n  - {exc}", file=sys.stderr)
                failed = True
                continue
        if not isinstance(expected_version, str) or not re.fullmatch(
            r"\d+\.\d+\.\d+", expected_version
        ):
            print(f"{root}: FAIL\n  - invalid Spec Kit version", file=sys.stderr)
            failed = True
            continue
        errors = validate(root, expected_version)
        if errors:
            failed = True
            print(f"{root}: FAIL", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"{root}: Spec Kit {expected_version} valid")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
