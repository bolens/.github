# Woodpecker validation transition

The native pipeline runs the existing locked `devenv test` in a disposable
Linux container on the shared CI site. It does not apply configuration to a
workstation. The clone and runtime images are immutable; there are no host
mounts, Docker sockets, privileged containers, or publishing secrets.

## CI organization

Use lowercase purpose phases in each repository's existing CI guide:

| Phase | Purpose |
| --- | --- |
| `validate` | Source, metadata, generated-file, lint and security contracts |
| `test` | Behavior, compatibility, runtime and platform checks |
| `site` | Site builds, links, metadata and accessibility |
| `publish` | Authorized artifact, package or site publication |

List applicable phases with descriptive check groups, the existing canonical
local command, native workflow/step, retained hosted owner and event or trust
boundary. Keep composite commands as the source of truth; an index can describe
their groups without splitting execution or copying their implementation.
Record current workflow and required-status names. A naming change joins source,
project config paths, protected checks, dependency selectors and release consumers
through the normal reviewed migration.

### This repository

`devenv test` runs `scripts/check-development.sh`, including the existing hooks,
Spec Kit checks, source lint and language fixtures. Use it as the complete local
native gate; the focused commands below remain useful during development.

| Phase | Check group / local command | Native workflow / step | Retained hosted owner / boundary |
| --- | --- | --- | --- |
| `validate` | Fleet tooling: `devenv test` | `woodpecker` / `development-environment` | PR, main push and native manual validation; no publisher credentials |
| `test` | Tooling fixtures: `python3 -m unittest discover -s tests -v` | Included in the same development gate | Spec Kit caller, macOS and actual Docker/editor checks retain their own hosted selection |
| `validate` | Workflow syntax/security: `actionlint`; `zizmor --offline --min-severity medium --min-confidence medium .github` | Included in the same development gate | Manual hosted fallbacks and CodeQL keep their existing triggers |

Reviewed `main` delivers shared configuration. Reusable caller updates and local
installation remain separately scoped actions; this repository has no versioned
artifact or site publisher.

## Delivery

Require `ci/woodpecker/pr/woodpecker` and the retained hosted Development
environment result before squash merging, then verify the genuine merged-main
pipeline. Woodpecker runs workflow syntax/security, fleet tooling tests, managed
Spec Kit validation, and all five source-lint language fixtures through the
existing development gate. The duplicate hosted Validate, zizmor, and Source
lint jobs remain manual fallbacks. The dedicated hosted Spec Kit caller workflow exercises the actual reusable
validator on every PR and main push. It has no manual maintenance trigger;
manual validation retains the separate immutable caller. Reusable workflow
interfaces remain unchanged.

The hosted development gate retains macOS native checks and actual Linux Docker
and editor-image acceptance. It skips the duplicate Linux native invocation.
Administrative update automation and CodeQL keep their existing workflows.

Local validation is evidence for the source; it does not establish native
runner success. Failure leaves existing GitHub validation available. Recover
through a corrective PR, without changing live workstation configuration.

Review image pins monthly and after security releases against the official
registries. Existing dependency automation does not discover these Woodpecker
YAML image references; updates require a reviewed PR and native execution.

The rollout also combines the open compatible lint-tool, Actions and editor
image updates. Editor changes select the hosted development gate, which builds
the actual devcontainer Dockerfile and executes its post-create smoke as a
non-root user with no network, capabilities, or writable image filesystem.
This is separate from the Nix-generated Docker development image.
