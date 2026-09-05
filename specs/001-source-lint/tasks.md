# Tasks

- [x] Define explicit source ownership and lint contract.
- [x] Implement shared workflow, pinned tooling, and tracked-file selection.
- [x] Verify real valid/invalid fixtures for all five linters and the Fish regression.
- [x] Wire source-repository CI to exercise tooling before consumer adoption.

Hosted verification is recorded on the implementation PR. Each downstream
consumer's scope, current-head checks, and merge are tracked in the fleet audit;
this shared implementation does not imply that every caller has been migrated.
