# Shared GitHub Configuration Constitution

## Core Principles

### I. Reusable, Minimal Interfaces
Shared workflows and community files MUST remain small and composable. Project-specific build, test, release, and policy decisions belong in the consuming repository.

### II. Supply-Chain Safety
Workflow permissions MUST be least-privilege. Third-party actions MUST be pinned immutably, untrusted pull-request code MUST NOT receive secrets, and reusable workflow inputs MUST be validated.

### III. Backward-Compatible Consumers
Changes to reusable workflow inputs, outputs, permissions, or behavior MUST account for existing callers. Breaking changes require an explicit migration and a coordinated rollout of immutable caller references through reviewed pull requests.

### IV. Focused Verification
Every workflow change MUST be syntax-checked and, where practical, exercised by a representative caller. Documentation and examples MUST match the published interface.

## Governance

This constitution governs shared defaults and workflows. Repository-local guidance governs consumers. Amendments require rationale, review of downstream impact, and a version update.

**Version**: 1.0.1 | **Ratified**: 2026-08-15 | **Last Amended**: 2026-09-05
