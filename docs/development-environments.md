# Development environments

[Documentation](README.md)

Install [Nix and devenv](https://devenv.sh/getting-started/), then run from this checkout:

```sh
devenv shell
repo-check
# Or run the same portable gate non-interactively:
devenv test
```

The shell supplies Node 24, Python, Ruff, Bash, jq, ShellCheck, actionlint, Zizmor, and GNU utilities. `repo-check` installs the existing npm lockfile for source lint, runs the native pre-push and Spec Kit checks, and tests real lint tools against valid and invalid fixtures. Bootstrap tests use disposable repositories. npm installation requires network access. Reusable workflow interfaces and consumer pins remain unchanged.

The Nix shell currently resolves Ruff 0.17.2 through its lockfile. Hosted source
lint and the editor image pin Ruff 0.17.5. Use Ruff 0.17.5 for exact hosted
Python-lint reproduction.

Commit `devenv.lock` with deliberate input updates. Local state and `devenv.local.nix` / `devenv.local.yaml` overrides are ignored. Existing Nix cache settings are used without changing daemon trust.

## Docker and Podman

Build and load the development image, then run a command with a local engine:

```sh
python3 scripts/development-container.py build podman
python3 scripts/development-container.py run podman -- bash scripts/check-development.sh
# Substitute docker for podman to use Docker.
```

Omit the command for an interactive Bash shell. The helper mounts the checkout at `/workspace`, runs with the caller's UID/GID, and uses Podman's keep-id mapping. It forwards arguments and exit status without constructing a shell command. These mounts require a local engine with access to the checkout path; remote Docker daemons need their own source transfer. Paths containing commas are rejected because they cannot be represented by this mount syntax.

The image contains tools, not checkout files. Build archives live under `.devenv/containers/` and are never uploaded by the helper.

## Apple container

[Apple container](https://github.com/apple/container) requires a supported Apple-silicon Mac. Start its runtime according to Apple's installation guide. With a Linux Nix builder configured:

```sh
python3 scripts/development-container.py build apple
python3 scripts/development-container.py run apple -- bash scripts/check-development.sh
```

The helper exports an OCI archive and uses `container image load`. Native ARM Macs target `aarch64-linux`; x86 Linux builds target `x86_64-linux`. [Building Linux images from macOS requires a Linux builder](https://devenv.sh/containers/). This workflow does not assume Apple container implements Docker Compose or Docker's daemon API.

Apple execution is not verified by Linux tests. The environment validates source and tooling. Existing reusable workflow callers remain governed by their own repository checks. This development workflow validates the shared tooling repository and does not deploy changes to consumers.

## Locked toolchain upgrades

CI uses devenv 2.4.0 at its immutable upstream commit. The lock update preserves
unrelated inputs and explicitly retains the existing git-hooks input contract.
The matching nix2container update removes deprecated platform aliases.
The fixed CI CLI invocation accepts only its reviewed upstream cache settings;
repository flakes do not receive global configuration trust. Disposable Nix
steps retain the image's standard `nixbld` users so builds do not run as root or
leave Go telemetry files in Nix's placeholder home.
