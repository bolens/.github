# Agent guidance

[Documentation](docs/README.md) maps architecture, deployment, state, and document ownership.

Read [.specify/memory/constitution.md](.specify/memory/constitution.md) before changing shared workflows.

- Use Spec Kit for new capabilities, architecture, security-sensitive behavior,
  migrations, and coordinated multi-file changes. Keep narrow fixes, dependency
  updates, prose edits, and release housekeeping in the normal repository
  workflow unless their risk warrants a written specification.
- Treat workflow inputs, permissions, secrets, and pull-request execution as
  security boundaries. Pin third-party actions immutably.
- Preserve existing reusable-workflow callers; interface changes need migration
  notes and representative validation.
- Do not publish releases, tags, or repository settings unless requested.

- Run `bash scripts/install-git-hooks` once per clone; hooks mirror workflow and Spec Kit validation locally.
- Keep [docs/spec-kit.md](docs/spec-kit.md), the reusable Spec Kit workflows, bootstrap template,
  and validator aligned. Callers pin this repository by immutable commit.

## Context and handoffs

- Search before reading. Use bounded source excerpts for exploratory reads over
  350 lines, and inspect required guidance and actual source before editing.
- When delegation is permitted, assign a bounded question or output, paths, and
  check. Return source locations, changes, and verification gaps for final review.
- Keep durable corrections in the [project guide](.specify/memory/project-guide.md)
  or owning contract. Replace superseded advice and read it before reuse.
  Temporary progress belongs in task notes. Preserve existing authority rules.
