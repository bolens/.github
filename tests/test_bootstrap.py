"""Exercise bootstrap without downloading or running upstream tooling."""
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class BootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'repository with spaces'
        self.env = dict(os.environ)
        # Git hooks export repository-local variables, including GIT_DIR.
        local_vars = subprocess.check_output(
            ['git', 'rev-parse', '--local-env-vars'], text=True).splitlines()
        for key in local_vars:
            self.env.pop(key, None)
        subprocess.run(['git', 'init', '-q', str(self.repo)], check=True, env=self.env)
        self.bin = self.root / 'bin'
        self.bin.mkdir()
        specify = self.bin / 'specify'
        specify.write_text('''#!/usr/bin/env python3
import os, shutil
from pathlib import Path
source = Path(os.environ['BOOTSTRAP_FIXTURE'])
for name in ('.specify', '.agents'):
    shutil.copytree(source / name, Path.cwd() / name)
''')
        specify.chmod(0o755)
        self.env.update(PATH=f'{self.bin}:{os.environ["PATH"]}',
                        BOOTSTRAP_FIXTURE=str(ROOT))

    def bootstrap(self, *args):
        return subprocess.run(['bash', str(ROOT / 'scripts/bootstrap-spec-kit'),
                               *args], env=self.env, text=True, capture_output=True)

    def test_step_cron_and_repository_with_spaces(self):
        result = self.bootstrap('--tooling-ref', 'a' * 40, '--cron',
                                '17 */6 * * *', str(self.repo))
        self.assertEqual(result.returncode, 0, result.stderr)
        text = (self.repo / '.github/workflows/spec-kit.yml').read_text()
        self.assertIn('17 */6 * * *', text)
        self.assertIn('a' * 40, text)
        self.assertNotIn('CENTRAL_WORKFLOW_REF', text)

    def test_missing_option_values_report_usage(self):
        for option in ('--tooling-ref', '--cron'):
            with self.subTest(option=option):
                result = self.bootstrap(option)
                self.assertEqual(result.returncode, 2)
                self.assertIn('usage:', result.stderr)

    def test_extra_repository_is_rejected_before_changes(self):
        result = self.bootstrap('--tooling-ref', 'a' * 40,
                                str(self.repo), str(self.repo))
        self.assertEqual(result.returncode, 2)
        self.assertFalse((self.repo / '.specify').exists())


if __name__ == '__main__':
    unittest.main()
