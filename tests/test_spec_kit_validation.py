"""Malformed consumer metadata must fail without escaping the repository."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'consumer'
        for directory in ('.specify', '.agents'):
            shutil.copytree(ROOT / directory, self.root / directory)

    def validate(self, *roots):
        return subprocess.run(['python3', str(ROOT / 'scripts/validate-spec-kit.py'),
                               *map(str, roots or (self.root,))],
                              text=True, capture_output=True)

    def update(self, name, change):
        path = self.root / name
        data = json.loads(path.read_text())
        change(data)
        path.write_text(json.dumps(data))

    def test_existing_integration_passes(self):
        result = self.validate()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_malformed_nested_settings_fail_and_next_repository_runs(self):
        for settings in (None, [], {'codex': None}, {'codex': {'parsed_options': []}}):
            with self.subTest(settings=settings):
                self.update('.specify/integration.json',
                            lambda data: data.update(integration_settings=settings))
                result = self.validate(self.root, ROOT)
                self.assertEqual(result.returncode, 1)
                self.assertNotIn('Traceback', result.stderr)
                self.assertIn('valid', result.stdout)

    def test_manifest_paths_cannot_escape_or_follow_symlinks(self):
        outside = self.root.parent / 'external.txt'
        outside.write_text('fixture')
        (self.root / 'link').symlink_to(outside)
        for name in ('../external.txt', str(outside), 'link'):
            with self.subTest(name=name):
                import hashlib
                self.update('.specify/integrations/codex.manifest.json',
                            lambda data: data.update(files={name: hashlib.sha256(b'fixture').hexdigest()}))
                result = self.validate()
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn('unsafe managed path', result.stderr)
                self.assertNotIn('Traceback', result.stderr)

    def test_invalid_utf8_is_reported_without_aborting_other_repositories(self):
        (self.root / '.specify/integration.json').write_bytes(b'\xff')
        result = self.validate(self.root, ROOT)
        self.assertEqual(result.returncode, 1)
        self.assertNotIn('Traceback', result.stderr)
        self.assertIn('valid', result.stdout)
