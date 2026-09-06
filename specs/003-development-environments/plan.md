# Implementation plan

Pin devenv/nixpkgs and supply Node 24, Python, Ruff, Bash, GNU utilities, jq,
ShellCheck, actionlint, and Zizmor. Install the existing source-lint npm lockfile and
wrap established commands; add engine argument regressions without changing the
shared lint or reusable workflow contracts. Validate native Linux and rootless
Podman, then native macOS and actual Docker in this repository's CI.

Use filtered triggers, read-only permissions, superseded-run cancellation, and an
always-reporting result. Follow protected PR delivery and verify main afterward.
This repository publishes no versioned release for development tooling.
