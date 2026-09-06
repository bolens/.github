#!/usr/bin/env python3
"""Regenerate managed integration files while checking project-owned guidance."""
import argparse
from pathlib import Path
import re
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('upstream_sha')
    args = parser.parse_args()
    if not re.fullmatch(r'[0-9a-f]{40}', args.upstream_sha):
        parser.error('upstream revision must be a lowercase 40-character commit SHA')
    memory = Path('.specify/memory')
    paths = {path for path in memory.rglob('*') if path.is_file()
             and path != memory / '.constitution-template.json'}
    paths.add(memory / 'constitution.md')
    if Path('AGENTS.md').exists():
        paths.add(Path('AGENTS.md'))
    try:
        before = {path: path.read_bytes() for path in paths}
    except OSError as error:
        print(f'Cannot snapshot project guidance: {error}', file=sys.stderr)
        return 1
    result = subprocess.run([
        'uv', 'tool', 'run', '--from',
        f'git+https://github.com/github/spec-kit.git@{args.upstream_sha}',
        'specify', 'init', '--here', '--force', '--non-interactive',
        '--integration', 'codex', '--integration-options=--skills',
        '--script', 'sh', '--ignore-agent-tools',
    ], check=False)
    if result.returncode:
        return result.returncode
    changed = []
    for path, original in before.items():
        try:
            if path.read_bytes() != original:
                changed.append(path)
        except OSError:
            changed.append(path)
    for path in sorted(changed):
        print(f'Spec Kit regeneration changed project guidance: {path}', file=sys.stderr)
    return 1 if changed else 0


if __name__ == '__main__':
    raise SystemExit(main())
