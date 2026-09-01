# Agent guidance

Read `.specify/memory/constitution.md` before changing shared workflows.

- Treat workflow inputs, permissions, secrets, and pull-request execution as
  security boundaries. Pin third-party actions immutably.
- Preserve existing reusable-workflow callers; interface changes need migration
  notes and representative validation.
- Do not publish releases, tags, or repository settings unless requested.
