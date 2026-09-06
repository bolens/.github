# Repository documentation standard

[Documentation](README.md) · [Contributing](../CONTRIBUTING.md) ·
[Delivery policy](../RELEASING.md)

Each maintained repository keeps one linked documentation entry point. Use its
existing `docs/README.md`, `documents/README.md`, or `DOCUMENTATION.md` rather than
creating a competing index. Keep the structure consistent and the content specific
to the repository.

## What to document

| Topic | Keep | Link instead of copying |
| --- | --- | --- |
| Agent guidance | Constraints, authority, generated-file ownership, task-specific reading | Architecture and validation guides |
| Architecture | Boundaries, data flow, invariants, rationale, failure behavior | Directory trees, symbols, manifests |
| Deployment | Artifact, target, persistence, verification, recovery limits | Release workflow and existing operator runbook |
| Database and state | Ownership, durability, compatibility, retention, restore requirements | Schema fields, migration code, storage defaults |
| Development and testing | Environment constraints, test isolation, evidence limits | Native task definitions and CI |
| Security | Trust boundaries and private-data handling | The owning security policy |

A small repository can cover these topics in short index sections. Split a topic
when it has enough independent detail to need its own guide. Do not create empty
database or deployment documents for a repository that has neither. Bootstrap
repositories must distinguish planned capabilities from implemented automation.

## Prevent drift

Give every contract one owner. Link from the README and agent guide to the index,
from the index to each maintained guide, and from guides back to the index or a
related owner. Use relative repository links for local content and stable heading
anchors for focused references. Preserve useful anchors when shortening a guide.

Update prose with the source change that invalidates it. Regenerate managed docs
from their template, catalog, schema, or source help. Historical specs and dated
audits retain their assessed revision and evidence limits. They do not override
current implementation contracts.

Check changed Markdown, local paths, anchors, and index coverage. Use existing
documentation and generation checks where available. Report remote-link or live
deployment verification separately. Cross-links improve navigation but do not
prove two descriptions agree, so review the owning source when behavior changes.
