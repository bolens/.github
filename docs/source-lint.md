# Source lint contract

Use this gate for maintained source that lacks an equivalent native lint check.
Keep native Go vet/golangci-lint, Rust Clippy, TypeScript/ESLint, PSScriptAnalyzer,
QML, Fish, container, and repository-specific checks in their owning projects.

Call `reusable-source-lint.yml` at an immutable commit and pass the same SHA as
`tooling-ref`. The caller grants only `contents: read`, runs on every PR and its
default-branch pushes, and defines `.github/source-lint.json`. Each language key
contains nonempty Git-path globs; `*` also matches directory separators. Enabled
checks must match at least one tracked file. `exclude` contains reviewed glob
exclusions and `notes` explains imported/generated ownership or native coverage.

Supported checks:

- `python`: Ruff 0.15.20 syntax and Pyflakes correctness (`E9,F`), without formatting.
- `shell`: ShellCheck warning/error diagnostics for selected sh/Bash files and shebangs.
- `javascript`: ESLint recommended logic checks. Host globals and unused exported
  entry points are left to native type/QML checks, so `no-undef` and `no-unused-vars`
  are disabled. Empty catch blocks, deliberate control-character regexes, and
  regex whitespace/escape style are allowed. Other recommended logic rules block. A QML `.pragma library` line is omitted for ECMAScript parsing.
- `css`: Stylelint correctness checks for browser CSS. GTK/Waybar styles need their
  native configuration; do not send them through the browser rule set.
- `markdown`: malformed heading/link/emphasis/code-span checks. Formatting, line
  lengths, and stylistic conventions remain repository-local.

Only tracked files are read. Symlink sources are rejected. Spec Kit managed
`.specify/` and `.agents/` files retain their dedicated hash/integration validation.
Globs are arguments, never shell programs. Missing tools, invalid configuration,
empty enabled selections, or any linter failure fail the job. Dependency installs
use an npm lockfile with lifecycle scripts disabled. The gate never deploys,
changes live configuration, or requires secrets.

To reproduce locally, use a checkout of the same shared SHA and install its tools:

```sh
npm ci --ignore-scripts --prefix /path/to/shared/tools/source-lint
# Install Ruff 0.15.20 and ShellCheck through your normal tool manager.
python3 /path/to/shared/scripts/lint-source.py /path/to/repo
```

`--list` prints the selected tracked files without running linters. Review this
selection when adding languages or exclusions. No tests or compiler/type checks
are replaced by this gate. New required status checks should only be enabled
after a representative current-head run passes.

Tool references: [Ruff rules](https://docs.astral.sh/ruff/rules/),
[ESLint configuration](https://eslint.org/docs/latest/use/configure/configuration-files),
and [GitHub workflow reuse](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).
