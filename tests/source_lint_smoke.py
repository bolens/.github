"""Exercise real tools; run after installing the shared lint dependencies."""
from pathlib import Path
import json
import os
import subprocess
import tempfile

for key in list(os.environ):
    if key.startswith("GIT_"):
        del os.environ[key]

TOOL = Path(__file__).resolve().parents[1] / "scripts/lint-source.py"
CASES = {
    "python": ("sample.py", "print('ok')\n", "print(undefined_name)\n"),
    "javascript": ("sample.js", "console.log('ok');\n", "function f() { return 1; console.log('unreachable'); }\n"),
    "css": ("sample.css", "a { color: red; }\n", "a { colour: red; }\n"),
    "markdown": ("sample.md", "# Title\n", "# Title\n\n[empty]()\n"),
    "shell": ("sample.sh", "#!/bin/sh\nprintf '%s\\n' ok\n", "#!/bin/sh\necho $undefined\n"),
}
for kind, (name, good, bad) in CASES.items():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory) / "source with spaces 雪"
        root.mkdir()
        (root / ".github").mkdir()
        (root / ".github/source-lint.json").write_text(json.dumps({kind: ["*"]}))
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        source = root / name
        source.write_text(good)
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        result = subprocess.run(["python3", str(TOOL), str(root)], capture_output=True, text=True)
        assert result.returncode == 0, (kind, result.stdout, result.stderr)
        source.write_text(bad)
        result = subprocess.run(["python3", str(TOOL), str(root)], capture_output=True, text=True)
        assert result.returncode != 0, (kind, "broken source passed")
        print(kind, "valid passed, invalid rejected")
