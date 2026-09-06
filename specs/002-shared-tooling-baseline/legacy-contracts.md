# Legacy capability contracts

Retrospective audit of `27cef0b` on 2026-09-06. This expands the earlier broad
baseline with caller-visible behavior. FR-006–008 in [spec.md](spec.md) identify
corrections discovered during this audit; the remaining contracts describe
existing behavior. The two original feature specs and development-environment
spec remain authoritative for their scopes.

## LC-001: Bootstrap

`scripts/bootstrap-spec-kit` accepts one repository, a required lowercase
40-character `--tooling-ref`, and optional `--cron` (default `17 7 * * 1`). Help
returns zero; unknown options, missing values, mutable references, and extra
repositories return usage status 2. Git must resolve the target worktree and
its porcelain status must be empty before upstream initialization runs.

The installed `specify` executable initializes in place, noninteractively and
forcibly, with Codex skills, Bash helpers, and ignored agent-tool discovery.
This does not install or choose a version of that executable. Bootstrap renders
`templates/spec-kit.yml`, substituting the same immutable tooling/workflow SHA
and JSON-quoting the cron scalar so quotes and backslashes remain data. Cron
syntax is ultimately checked by workflow validation. Paths containing spaces
are single arguments. Validation runs after generation; unresolved constitution
placeholders fail until the maintainer tailors governance. Bootstrap is not a
transaction and does not roll back generated files on failure.

## LC-002: Installation validation

`scripts/validate-spec-kit.py` accepts zero or more repositories (default current
working directory) and `--expected-version`. Omitted or `current` derives each
repository's version; an explicit version must match numeric `major.minor.patch`.
Every repository gets a success or failure diagnostic; any failure returns 1.
JSON metadata roots must be objects. Integration selects only Codex, as both
installed and default integration, with Bash and enabled skills. Initialization
options retain sequential numbering, in-place initialization, Codex skills,
Bash, and the expected Spec Kit version.

Exactly `codex.manifest.json` and `speckit.manifest.json` are expected. Each must
match the version and map managed filenames to matching SHA-256 file content.
The constitution must have no configured unresolved placeholders and must match
the documented version/date metadata format. Dates are syntax-checked, not
calendar-validated. Generated Bash scripts undergo `bash -n` without execution.
This checks installation integrity, not feature completeness, package signatures,
or whether omitted manifest entries ought to exist upstream.

FR-008 adds controlled failures for malformed nested settings and invalid UTF-8
JSON, and rejects absolute paths, parent traversal, and symlink components before
reading managed content. A failure in one consumer does not suppress results for
other consumers. These are corrections to the inspected revision.

## LC-003: Reusable Spec Kit validation

`reusable-spec-kit.yml` requires `tooling-ref`; `expected-version` defaults to
`current`. It grants only `contents: read`, uses a five-minute Ubuntu job, checks
out caller and tooling separately with persisted credentials disabled, and runs
the tooling validator against the caller. Inputs enter shell commands through
environment variables and quoted arguments. FR-006 adds immutable-reference
validation before tooling checkout. No caller workflow interface changes.

## LC-004: Upstream update proposal

`reusable-spec-kit-update.yml` requires `tooling-ref`; `update-branch` defaults
to `automation/spec-kit-update`. Its ten-minute Ubuntu job needs contents and
pull-request writes using only the caller token. Caller checkout retains the
credentials needed for PR creation; tooling checkout does not. `.fleet-config`
is excluded locally from the candidate update.

The job resolves the latest stable GitHub Spec Kit release, strips leading `v`
for its version, and resolves the tag reference to a commit (including a single
annotated-tag dereference). The resulting SHA must be lowercase hex of length
40. An unchanged installed version skips installation, regeneration, validation,
and PR creation. A changed version installs uv without caching and invokes
upstream by the resolved commit, with the same Codex/Bash options as bootstrap.
Failures stop subsequent steps. Version comparison is equality, not an upgrade
ordering policy: an intentionally newer installed version is not special-cased.

The original job checked only constitution bytes. FR-007 introduces
`scripts/regenerate-spec-kit.py`: snapshot every pre-existing memory file except
upstream `.constitution-template.json`, plus an existing `AGENTS.md`; require the
constitution; run pinned upstream; reject changed or removed project files.
New files are permitted. Upstream nonzero status propagates. The disposable
checkout retains partial changes for diagnosis; it is not restored or published
on failure. FR-006 also rejects mutable tooling before checkout.

After successful regeneration the validator requires the resolved version.
The pinned PR action signs commits, uses the configured branch, deletes an
obsolete update branch according to its action policy, and supplies dependency
and automation labels plus release tag/SHA evidence. It opens a proposal; it
does not merge or prove that product features satisfy their specifications.
GitHub must allow Actions to create PRs. No live updater execution is necessary
to test regeneration with a fake upstream command.

## LC-005: Caller template and integration ownership

`templates/spec-kit.yml` and this repository's caller validate relevant Spec Kit,
Codex skill, workflow, and `AGENTS.md` changes on PRs/main pushes. A schedule or
manual `update` input selects update instead. Permissions are empty globally,
read-only for validation, and writes only for the updater. The caller cancels
superseded validation using workflow and full ref. Update jobs are not cancelled
by that group. Both remote workflow references and tooling references must name
the same immutable revision; consumer adoption happens through reviewed pin PRs.

Upstream templates, generated skills, scripts, and their manifests stay managed.
Local customization lives in project-owned memory and instructions. Existing
feature directories retain decisions and evidence; an installation pass must
never be presented as implementation completion. The guide, constitution,
`docs/spec-kit.md`, and register describe these separate responsibilities.

## LC-006: Workflow syntax and security audit

`reusable-actionlint.yml` has optional boolean `security-audit` default false.
Its read-only five-minute jobs disable persisted checkout credentials. The
syntax job downloads the centrally versioned Linux actionlint archive, verifies
its declared SHA-256 strictly, extracts the binary, and runs workflow lint.
Opt-in zizmor uses a pinned action and tool version, runs offline without
advanced-security publication, and blocks medium-or-higher severity and
confidence findings. Caller concurrency remains caller-owned.

## LC-007: Fish syntax

`reusable-fish.yml` has no inputs, reads contents, installs Fish on Ubuntu, and
syntax-checks every tracked `*.fish` path individually with `--no-execute`.
NUL-delimited Git output preserves whitespace in filenames. No files succeeds;
any invalid file fails. It does not source shell configuration or apply it to
an operator's session. The job timeout is ten minutes.

## LC-008: Pull-request path labels

`reusable-pr-labeler.yml` has no inputs, grants contents read and PR write, and
uses pinned `actions/labeler` with the caller token and `sync-labels: true`.
Repository-owned label configuration determines matching paths. The five-minute
job does not check out or execute PR code; action/API failures remain failures.
It changes labels, not assignees or requested reviewers.

## LC-009: Maintainer assignment

`reusable-auto-assign.yml`, its caller, `docs/auto-assignment.md`, and
[the original spec](../001-maintainer-assignment/spec.md) own assignment.
Only bolens repositories run; issues and PR-target events fetch current item
state, while scheduled/manual reconciliation paginates all open items. Missing
or invalid item numbers, unsupported events, and API failures reject. Closed
items and case-insensitive existing bolens assignments cause no write. Additive
assignment preserves co-assignees, includes bot/fork/maintainer authors, and
checks the API actually applied the assignee. There is no checkout, item-text
execution, review request, or content edit. The caller covers issue opened,
reopened, transferred and PR opened/reopened events, plus daily reconciliation.

## LC-010: Maintained source selection and lint

`reusable-source-lint.yml` requires a 40-character immutable `tooling-ref`, grants
contents read, and separately checks out source/tooling without credentials.
It installs pinned Node/Ruff and locked npm dependencies with lifecycle scripts
disabled, plus ShellCheck, then invokes `scripts/lint-source.py`.

The selector reads only tracked paths from an isolated Git environment and
`.github/source-lint.json`. Five language keys take nonempty glob strings;
`exclude` removes reviewed paths, and `notes` records ownership. Unknown keys,
invalid lists, zero configured languages, empty enabled selections, and selected
symlinks reject. Managed `.specify` and `.agents` files are excluded. Filename
suffixes or supported Python/Bash/sh shebangs determine applicable checks.
`--list` emits selections without linting. Commands receive arguments directly,
including space/Unicode paths, in batches of at most 100. Any linter failure
makes the final exit nonzero.

Python uses Ruff `E9,F`; shell uses ShellCheck warning severity. The Node driver
owns ESLint logic checks (host globals and unused entry points excluded), QML
pragma stripping with line preservation, CSS correctness rules, and the listed
Markdown syntax rules. `docs/source-lint.md`,
[the original spec](../001-source-lint/spec.md), and real-tool smoke fixtures
remain the rule-level contract. Native type, compiler, QML, GTK, and product
checks remain consumer-owned.

## LC-011: Repository validation and developer adapters

`ci.yml` runs unit tests, installation validation, actionlint, offline zizmor,
maintained-source lint and deliberate valid/invalid real-tool fixtures. Hooks
check staged whitespace and relevant integration/workflow files before commit;
pre-push checks all integration JSON/Bash plus tests and workflow lint.
`scripts/install-git-hooks` installs these hooks locally. Development setup and
Docker/Podman/Apple command contracts belong to
[003-development-environments](../003-development-environments/spec.md), its
fixtures, `devenv.nix`, `scripts/development-container.py`, and the OS matrix.
No published image or live host configuration is implied by these local adapters.

## LC-012: Community policy and delivery

`CONTRIBUTING.md` requires focused changes, native checks, and squash PR delivery.
`RELEASING.md` defines exact-head and post-merge evidence, consumer compatibility,
continuous delivery, and corrective/revert recovery. This repository publishes
no versioned release. `SECURITY.md` directs sensitive reports to private reporting
or a minimal contact request; it makes no response-time promise. `SUPPORT.md`
requires reproducible, sanitized reports and excludes urgent operational support.
The issue form requires description, reproduction, and revision; environment and
sanitized logs are optional. Blank issues remain enabled. The PR template asks
for summary, validation, and risk. None of these files authorizes operational
application, settings changes, or sharing private evidence.
