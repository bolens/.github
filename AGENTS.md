# Agent guidance

Before Spec Kit planning or implementation, read
`.specify/memory/project-guide.md` with the project constitution. It maps
requirements to this repository's source, acceptance evidence, and validation.

Read `.specify/memory/constitution.md` before changing shared workflows.

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
- Keep `docs/spec-kit.md`, the reusable Spec Kit workflows, bootstrap template,
  and validator aligned. Callers pin this repository by immutable commit.
