# .github Spec Kit project guide

Shared GitHub workflows and community policy for the personal repository fleet.

Read this guide with `AGENTS.md` and `.specify/memory/constitution.md` before
specifying, planning, or implementing a substantial change. It is project-owned
guidance, not an upstream-managed template.

## Source and ownership map

- `.github/workflows/`
- `scripts/validate-spec-kit.py`
- `scripts/bootstrap-spec-kit`
- `templates/spec-kit.yml`
- `docs/spec-kit.md`

## Specification and plan decisions

Name the caller and reusable workflow boundary. Specify inputs, outputs, default
permissions, immutable action references, and behavior for untrusted pull requests. A
shared change must identify affected callers and preserve their existing interfaces or
include a reviewed migration.

## Acceptance evidence

Cover a valid caller, malformed input, missing permissions, and update failure. Verify
bootstrap and updater behavior in disposable repositories. Preserve project-owned memory
and instruction files while regenerating managed integrations.

## Validation and operational limits

```sh
python3 -m unittest discover -s tests -v
actionlint
zizmor --offline --min-severity medium --min-confidence medium .github
```

Representative caller CI is required for changed workflow behavior. Do not change
repository settings, expose secrets to PR code, or publish fleet-wide updates merely to
exercise a test.

## Working through Spec Kit

Use Spec Kit for new capabilities, architectural or security-sensitive changes,
migrations, and coordinated changes that need a written contract. Keep narrow fixes,
dependency updates, and prose maintenance in the normal PR workflow.

For a new feature, record observable acceptance criteria in `spec.md`, source ownership
and constitution checks in `plan.md`, and evidence-bearing work in `tasks.md` under the
feature directory created by Spec Kit. Resolve material unknowns before implementation.
Mark tasks complete only after their stated verification, and distinguish completed,
skipped, blocked, and manual checks. Retain completed feature documents as decision
history; do not backfill feature specifications for already finished code.

Keep `.specify/templates/`, `.specify/scripts/`, and generated Codex skills under their
integration manifests. Use this guide and the constitution for local customization.
Regenerate managed files through Spec Kit and verify that project-owned memory survives
updates. Follow `RELEASING.md` for push, merge, release or delivery, and recovery.
