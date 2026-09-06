# Fleet Spec Kit policy

Repositories use GitHub Spec Kit when behavior or design needs an explicit
contract before implementation. Use it for new capabilities, architectural
changes, security-sensitive behavior, migrations, and coordinated multi-file
changes. Skip it for narrow fixes, dependency updates, prose edits, and release
housekeeping unless their risk warrants a written specification.

Keep completed feature directories under `specs/` as decision history. Backfill
finished work when explicitly requested. Label those documents as retrospective
baselines, identify the inspected revision, and map requirements to source and
acceptance evidence. Distinguish observed behavior from corrective requirements.
Never imply that a retrospective specification preceded its implementation.

## Project-owned customization

Every repository keeps a tailored `.specify/memory/constitution.md` and
`.specify/memory/project-guide.md`, with the guide referenced from `AGENTS.md`.
The constitution states durable constraints. The guide maps specification and
planning decisions to real source files, acceptance cases, native validation,
operational limits, and the repository's `RELEASING.md`.

Review that map against the code before claiming setup is complete. Resolve
project placeholders and stale paths. Do not invent test commands, hardware
verification, or completed feature work. Record missing tools and manual checks
as limitations rather than passes. Subprojects need tracked guidance when root
instructions delegate to them.

Templates, shell helpers, and generated Codex skills are upstream-managed and
hash-checked. Their reusable placeholders are intentional. Put local rules in
project-owned memory instead of modifying managed files or their recorded
hashes. Verify project-owned memory survives regeneration when upgrading.

Feature implementation remains separate from installing Spec Kit. For new
features and requested retrofits, fill the spec, plan, and tasks with actual
decisions and evidence. Mark work complete only after its acceptance checks.
Record a failed, unavailable, or hardware-dependent check as such. Installation
validation does not prove that feature requirements are implemented. Empty
feature history is valid until a repository adopts feature planning or its
owner requests a retrospective baseline.

## Validation and updates

The reusable validation workflow checks:

- the expected Spec Kit version and Codex skills integration;
- both integration manifests and every managed-file hash;
- constitution metadata and unresolved placeholders; and
- Bash syntax for generated shell helpers.

Each caller runs validation only when Spec Kit files or repository guidance
change. Its weekly schedule resolves the latest stable upstream release to an
immutable commit, regenerates managed files, proves that pre-existing project-owned
memory and `AGENTS.md` were preserved, validates the result, and opens a squash-ready
pull request.

The repository setting **Allow GitHub Actions to create and approve pull
requests** must permit pull-request creation. The updater uses only the caller's
`GITHUB_TOKEN`; it has no fleet-wide credential.

Run the same validation locally:

```bash
python3 scripts/validate-spec-kit.py --expected-version current .
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

Tailor the generated constitution, create the project guide described above,
and link it from `AGENTS.md` alongside the workflow rule. Run the validator and
the repository's relevant checks before opening the pull request. Bootstrap
can report unresolved constitution placeholders until customization is complete.

## Superseded validation

The caller cancels older validation jobs for the same workflow and Git ref.
The update job has no cancellation group because it can write an update PR.
Keep this concurrency block in callers when updating their immutable pins;
reusable workflows inherit the caller workflow name and must not reuse its group.

Both reusable Spec Kit workflows reject mutable tooling references before checkout.
Regeneration checks all pre-existing memory files except upstream
`.constitution-template.json`, and existing `AGENTS.md`. Changed or removed project
guidance stops PR creation; inspect the disposable checkout and repair through the
normal update workflow. Partial generation is not rolled back automatically.
