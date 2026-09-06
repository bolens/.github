# Documentation

Shared GitHub workflow and community-policy contracts.

## Start here

| Need | Owning document |
| --- | --- |
| Use the project | [README.md](../README.md) |
| Change the repository | [AGENTS.md](../AGENTS.md) |
| Deliver or recover | [RELEASING.md](../RELEASING.md) |
| Plan substantial changes | [.specify/memory/project-guide.md](../.specify/memory/project-guide.md) |
| Non-negotiable constraints | [.specify/memory/constitution.md](../.specify/memory/constitution.md) |

## Architecture

Consumer repositories own product build, test, and release decisions. Reusable workflows own only
their declared inputs, permissions, and outputs. A shared change does not reach SHA-pinned callers
until those callers adopt it. Keep bootstrap templates, validators, and examples aligned through the
[Spec Kit contract](spec-kit.md).

## Deployment and recovery

[RELEASING.md](../RELEASING.md) owns rollout and recovery. Validate a representative caller before
adoption. Community defaults and workflow callers have different propagation rules, so verify the
affected consumer instead of treating a merge here as fleet delivery.

## Database and state

There is no application database. Integration manifests and project-owned memory have different
owners: regenerating Spec Kit must preserve memory. [Auto-assignment](auto-assignment.md) operates
on issue and PR metadata without executing contributor code.

## Documentation maintenance

Keep decisions, invariants, failure modes, and recovery requirements in the owning document. Link to
commands, defaults, schemas, and generated catalogs instead of copying them. Change the owner and
affected references together. Update this index when adding or moving a guide, and verify relative
links and heading anchors. Historical specs and audits describe their recorded revision, not current
runtime proof. A topic without an implementation stays explicitly unimplemented.

## Topic guides

- [Contributing](../CONTRIBUTING.md)
- [Security policy](../SECURITY.md)
- [Support](../SUPPORT.md)
- [Maintainer assignment](auto-assignment.md)
- [Development environments](development-environments.md)
- [Source lint contract](source-lint.md)
- [Fleet Spec Kit policy](spec-kit.md)

- [Repository documentation standard](documentation.md)
