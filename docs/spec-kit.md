# Fleet Spec Kit policy

Repositories use GitHub Spec Kit when behavior or design needs an explicit
contract before implementation. Use it for new capabilities, architectural
changes, security-sensitive behavior, migrations, and coordinated multi-file
changes. Skip it for narrow fixes, dependency updates, prose edits, and release
housekeeping unless their risk warrants a written specification.

Keep completed feature directories under `specs/` as decision history. Do not
create retroactive specifications for finished work.

## Validation and updates

The reusable validation workflow checks:

- the expected Spec Kit version and Codex skills integration;
- both integration manifests and every managed-file hash;
- constitution metadata and unresolved placeholders; and
- Bash syntax for generated shell helpers.

Each caller runs validation only when Spec Kit files or repository guidance
change. Its weekly schedule resolves the latest stable upstream release to an
immutable commit, regenerates managed files, proves that the constitution was
preserved, validates the result, and opens a squash-ready pull request.

The repository setting **Allow GitHub Actions to create and approve pull
requests** must permit pull-request creation. The updater uses only the caller's
`GITHUB_TOKEN`; it has no fleet-wide credential.

Run the same validation locally:

```bash
python3 scripts/validate-spec-kit.py --expected-version 1.0.3 .
```

From this repository, validate several checked-out repositories in one command:

```bash
python3 scripts/validate-spec-kit.py /path/to/repository [...]
```

## Bootstrap a repository

Install the current official `specify` CLI, find the immutable commit of the
current `bolens/.github` main branch, then run:

```bash
bash scripts/bootstrap-spec-kit \
  --tooling-ref <40-character-commit> \
  --cron '17 7 * * 1' \
  /path/to/clean/repository
```

Tailor the generated constitution and add the workflow rule from this
repository's `AGENTS.md`. Run the validator and the repository's normal checks
before opening the pull request.
