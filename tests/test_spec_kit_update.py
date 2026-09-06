"""Exercise update boundaries with disposable repositories and a fake uv."""
import os
import shutil
from pathlib import Path
import subprocess
import tempfile
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        memory = self.root / '.specify/memory'
        memory.mkdir(parents=True)
        for name in ('constitution.md', 'project-guide.md', 'custom.txt'):
            (memory / name).write_text('project-owned ' + name)
        (memory / '.constitution-template.json').write_text('{}')
        (self.root / 'AGENTS.md').write_text('project instructions')
        binary = self.root / 'bin'
        binary.mkdir()
        uv = binary / 'uv'
        uv.write_text('''#!/usr/bin/env python3
import os
from pathlib import Path
import sys
Path('invoked').write_text(' '.join(sys.argv[1:]))
target = os.environ.get('CHANGE')
if target:
    if os.environ.get('DELETE'):
        Path(target).unlink()
    else:
        Path(target).write_text('upstream replacement')
sys.exit(int(os.environ.get('FAIL', '0')))
''')
        uv.chmod(0o755)
        self.env = dict(os.environ, PATH=f'{binary}:{os.environ["PATH"]}')

    def run_update(self, sha='a' * 40, **env):
        return subprocess.run(['python3', str(ROOT / 'scripts/regenerate-spec-kit.py'), sha],
                              cwd=self.root, env=dict(self.env, **env),
                              capture_output=True, text=True)

    def test_preserved_memory_and_upstream_metadata_update(self):
        result = self.run_update(CHANGE='.specify/memory/.constitution-template.json')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('git+https://github.com/github/spec-kit.git@' + 'a' * 40,
                      (self.root / 'invoked').read_text())
        self.assertEqual((self.root / 'AGENTS.md').read_text(), 'project instructions')

    def test_overwrite_and_removal_of_each_project_file_fail(self):
        for name in ('AGENTS.md', '.specify/memory/constitution.md',
                     '.specify/memory/project-guide.md', '.specify/memory/custom.txt'):
            for delete in ('', 'yes'):
                with self.subTest(name=name, delete=delete):
                    path = self.root / name
                    path.write_text('preserved original')
                    result = self.run_update(CHANGE=name, DELETE=delete)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(name, result.stderr)
                    path.write_text('preserved original')

    def test_upstream_failure_propagates(self):
        result = self.run_update(FAIL='17')
        self.assertEqual(result.returncode, 17, result.stderr)

    def test_invalid_revision_never_runs_upstream(self):
        for sha in ('main', 'v1.0.4', 'a' * 39, 'A' * 40, 'a' * 40 + '\n'):
            with self.subTest(sha=sha):
                self.assertNotEqual(self.run_update(sha).returncode, 0)
                self.assertFalse((self.root / 'invoked').exists())

    def test_workflow_invokes_the_preservation_guard(self):
        tooling = self.root / '.fleet-config/scripts'
        tooling.mkdir(parents=True)
        shutil.copy2(ROOT / 'scripts/regenerate-spec-kit.py', tooling)
        text = (ROOT / '.github/workflows/reusable-spec-kit-update.yml').read_text()
        block = text.split('      - name: Regenerate Spec Kit', 1)[1]
        script = textwrap.dedent(block.split('        run: |\n', 1)[1].split(
            '      - name: Validate update', 1)[0])
        result = subprocess.run(['bash', '-c', script], cwd=self.root,
                                env=dict(self.env, SPEC_KIT_SHA='a' * 40,
                                         CHANGE='.specify/memory/project-guide.md'),
                                text=True, capture_output=True)
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn('project-guide.md', result.stderr)

    def test_both_workflows_reject_mutable_tooling_before_checkout(self):
        for name in ('reusable-spec-kit.yml', 'reusable-spec-kit-update.yml'):
            text = (ROOT / '.github/workflows' / name).read_text()
            start = text.index('      - name: Validate tooling revision')
            end = text.index('      - name: Checkout fleet validator')
            self.assertLess(start, end)
            block = text[start:end].split('        run: |\n', 1)[1]
            script = textwrap.dedent(block)
            for ref in ('a' * 40, 'main', 'a' * 40 + '\n', 'A' * 40):
                with self.subTest(workflow=name, ref=ref):
                    result = subprocess.run(['bash', '-c', script],
                                            env=dict(self.env, TOOLING_REF=ref),
                                            capture_output=True)
                    self.assertEqual(result.returncode == 0, ref == 'a' * 40)
