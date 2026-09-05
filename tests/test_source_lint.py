import importlib.util
import os
from unittest import mock
from pathlib import Path
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("source_lint", Path(__file__).resolve().parents[1] / "scripts/lint-source.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class SelectionTests(unittest.TestCase):
    def setUp(self):
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        patch = mock.patch.dict(os.environ, environment, clear=True)
        patch.start()
        self.addCleanup(patch.stop)
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)

    def add(self, name, text="x = 1\n"):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        subprocess.run(["git", "add", "--", name], cwd=self.root, check=True)

    def test_tracks_spaces_and_unicode_but_not_untracked_or_managed(self):
        self.add("scripts/with space 雪.py")
        self.add(".specify/template.py")
        (self.root / "untracked.py").write_text("bad")
        self.assertEqual(MODULE.select(self.root, {"python": ["*.py"]}), {"python": ["scripts/with space 雪.py"]})

    def test_empty_and_unknown_configuration_fail(self):
        for config in [{}, {"pythno": ["*"]}, {"python": ["*.py"]}, {"python": "*.py"}]:
            with self.subTest(config=config), self.assertRaises(ValueError):
                MODULE.select(self.root, config)

    def test_exclusions_preserve_other_sources(self):
        self.add("vendor/example.py")
        self.add("scripts/check.py")
        self.assertEqual(MODULE.select(self.root, {"python": ["*.py"], "exclude": ["vendor/*"]}), {"python": ["scripts/check.py"]})

    def test_symlink_source_rejected(self):
        (self.root / "link.py").symlink_to("/etc/passwd")
        subprocess.run(["git", "add", "link.py"], cwd=self.root, check=True)
        with self.assertRaises(ValueError):
            MODULE.select(self.root, {"python": ["*.py"]})

    def test_extensionless_bash_selected(self):
        self.add("scripts/check", "#!/usr/bin/env bash\necho ok\n")
        self.add("scripts/data", "not shell\n")
        self.assertEqual(MODULE.select(self.root, {"shell": ["scripts/*"]}), {"shell": ["scripts/check"]})

    def test_inherited_git_context_cannot_redirect_selection(self):
        self.add("owned.py")
        with mock.patch.dict(os.environ, {"GIT_DIR": "/nonexistent/git", "GIT_INDEX_FILE": "/nonexistent/index"}):
            self.assertEqual(MODULE.select(self.root, {"python": ["*.py"]}), {"python": ["owned.py"]})

    def test_direct_shell_and_python_shebangs_are_selected(self):
        self.add("scripts/shell", "#!/bin/bash\necho ok\n")
        self.add("scripts/python", "#!/usr/bin/env -S python3 -u\nprint('ok')\n")
        self.assertEqual(MODULE.select(self.root, {"shell": ["*"], "python": ["*"]}), {
            "shell": ["scripts/shell"], "python": ["scripts/python"]})
