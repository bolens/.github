# Feature specification: Shared workflow and Spec Kit integration contracts

**Created**: 2026-09-05
**Status**: Retrospective baseline
**Inspected revision**: `59981d29243adcec608e045188a9219db62a7605`
**Input**: The owner requested a fleet-wide Spec Kit retrofit and implementation audit.

Shared workflows provide reusable fleet tooling while consumer repositories retain their native product gates.

This specification records existing contracts after implementation. It does not
claim that the original work followed Spec Kit. New behavior requires a separate
change contract. Existing feature specifications remain authoritative within their
own scope.

## User scenarios and testing

### User story 1: Use the supported interface (P1)

A user selects the documented entry point.

**Acceptance**: Its outputs and failure behavior follow the source and acceptance mapping.

### User story 2: Handle invalid input (P2)

Inputs or dependencies fail validation.

**Acceptance**: The named negative fixtures retain the rejection and recovery contracts.

### User story 3: Maintain the implementation (P3)

A maintainer changes a supported contract.

**Acceptance**: Update its authoritative source, documentation, and tests together.

## Requirements

- **FR-001**: Bootstrap MUST require an immutable tooling revision and clean worktree before installing the documented Codex integration.
- **FR-002**: Integration validation MUST check version, options, manifests, managed hashes, governance metadata, and Bash syntax.
- **FR-003**: Source lint MUST select tracked configured sources, reject invalid or empty configurations and unsafe symlinks, and preserve imported/generated exclusions.
- **FR-004**: Reusable workflows MUST preserve immutable tooling references, explicit permissions, caller contracts, and untrusted-event boundaries.
- **FR-005**: Maintainer assignment MUST use the documented account and event policy without interfering with excluded automation.

## Success criteria

- **SC-001**: Every requirement has a named source owner and acceptance check in `coverage.md`.
- **SC-002**: The listed native checks pass for the reviewed candidate, with unavailable environments and operational checks recorded separately.
- **SC-003**: Retrofitting preserves existing interfaces and completed specifications. Any confirmed implementation gap is corrected under an explicit requirement before it is marked complete.

## Edge cases and operational limits

No consumer pins or workflow interfaces change. Scheduled update PR delivery is separate from product implementation and does not imply all consumer features were tested.
