# Shared tooling development environment

Provide a locked devenv shell and source-free Docker, rootless Podman, and Apple
container adapters for developing this repository. Preserve all reusable workflow
inputs, outputs, permissions, immutable references, and existing caller behavior.
This new repository-local workflow requires no consumer pin migration.

Run the native Python, actionlint, Zizmor, Spec Kit and source-lint checks, including
real-tool fixtures that accept valid source and reject broken source. Use disposable
repositories for bootstrap tests. Images must exclude checkout content and secrets;
local runs preserve caller ownership and failures. Apple execution requires a
supported Mac and Linux Nix builder and remains unverified here.
