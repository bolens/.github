# Release Playbook Standard

[Documentation](docs/README.md)

The `.github` repository continuously delivers shared community files and reusable
workflows from protected `main`; it does not publish versioned artifacts. Changes
require local workflow lint, a representative caller check, a reviewed squash
merge, and verification that existing callers remain compatible. Recover through
a corrective or revert pull request; never patch consuming repositories around a
broken shared interface without documenting the migration.

This is the baseline for repositories owned by `bolens`. Each active,
non-empty repository keeps a root `RELEASING.md` that applies this standard to
its own release or deployment model.

## Required decisions

Every repository playbook must state:

- the branch push, PR review, squash merge, and post-merge verification path;
- whether it publishes versioned releases or continuously delivers `main`;
- the authoritative version source, when one exists;
- the exact local validation command and required GitHub checks;
- which artifacts, packages, images, sites, or configurations are delivered;
- who or what performs publication;
- how to verify the delivered result; and
- how to stop safely and recover from a partial or faulty delivery.

Commands must name real repository entry points. Do not replace a native task
runner with a long list of underlying tools.

## Push and merge

These steps apply to every change, including documentation, automation, and
release preparation. Repository playbooks supply the local validation and
publication commands.

1. Fetch the intended GitHub remote and branch from its current default branch
   in a clean worktree. Preserve unrelated local work. Confirm the push remote,
   target repository, base branch, and feature branch before publication.
2. Run the relevant local checks and installed hooks. Review the complete diff
   for secrets, private data, generated noise, and unrelated changes. Commit
   each coherent change separately and stage only its intended paths.
3. Push only the feature branch with
   `git push --set-upstream <github-remote> HEAD`. Never push the default branch,
   use a force push, skip a failing hook, or bypass branch protection. Hooks
   must not implicitly perform live or graphical checks. Use the repository's
   documented opt-in for those checks when authorized.
4. Open a pull request against the intended default branch. Describe the final
   behavior, validation results, limitations, and release implications. Review
   the full diff separately from implementation and address actionable feedback.
5. Require all applicable checks to pass on the current PR head and resolve
   review conversations. After a new push, inspect checks for the new head.
   A queued merge is not evidence that checks have passed or the PR has merged.
6. Squash-merge without bypassing protection. Confirm the resulting default
   branch SHA, wait for its applicable checks, and delete the merged feature
   branch after verifying no unmerged work remains.
7. Follow the repository's publication section only when the change needs a
   release or deployment and that action is authorized. Existing authorization
   carries forward. A merge alone does not prove publication succeeded.

Record the PR, merged SHA, checks, and any delivered artifact or deployment.
Diagnose failed checks before retrying. Repair source through a corrective PR
instead of rewriting published history.

## Execution evidence and retries

Keep each repository's native validation commands. For work spanning repositories
or long checks, record the candidate revision, owned paths, acceptance conditions,
dependencies, command results, and delivery state. A result from an older revision,
a skipped test, or a completed subprocess does not establish all acceptance
conditions. Recheck affected evidence after source, toolchain, or environment changes.

Use the [fleet execution-evidence contract](https://github.com/bolens/agent-skills/blob/main/skills/audit-repo-fleet/references/execution-evidence.md)
for private task records, bounded command execution, explained retries, and joins
between dependent work. Its optional helper records evidence in each worktree's
Git directory and adds no runtime dependency to the maintained application.
Do not copy private logs, source caches, or fleet inventories into public commits.

When returning to earlier maintenance, compare repository identity, candidate,
and check coverage before reporting progress. Separate proposed work, agent
completion claims, observed checks, and delivered changes. Several records of
one fix are one event. Missing or failed observations remain unknown. Before
adding a recurring process, state the failure it addresses, a measurable baseline,
and a reassessment point in existing task notes. Use the
[audit comparison guidance](https://github.com/bolens/agent-skills/blob/main/skills/audit-repo-fleet/references/comparing-runs.md)
to preserve counterevidence and decide whether the process helped.

Run independent checks together only when their writable state and external
resources are isolated. Serialize shared writers and generators. Delegation remains
subject to session authorization. Diagnose failures before retrying an unchanged
candidate, set finite attempt and time limits, and continue independent work when
a prerequisite is blocked. Require observed checks and review outcomes before the
existing merge and publication gates. Tests and review do not guarantee zero defects.

## Shared release rules

1. Start from the latest default branch in a clean worktree. Review staged
   paths for credentials, runtime state, generated noise, and unrelated work.
2. Put release preparation through a pull request. Do not push directly to the
   protected default branch or bypass required checks. Use the repository's
   required squash merge.
3. Run the documented local release gate before opening the pull request. CI
   must pass on the PR and, when a tag workflow gates on the merged SHA, on the
   resulting default-branch commit.
4. Update user-facing changelog entries for behavior, compatibility, security,
   migration, and operator-workflow changes. Leave routine dependency and
   test-only detail in Git history.
5. For manual semantic versions, derive the tag from the authoritative version
   source and create a signed annotated `vX.Y.Z` tag only after the release PR
   is merged. Automated versioning tools remain authoritative where declared.
6. Never move or overwrite a published tag or artifact. If a published release
   is faulty, document the impact and ship a corrective release. A tag may be
   replaced only while its release is still private/draft and no consumer can
   have relied on it.
7. Publishing credentials stay in the repository's approved secret store.
   Release output and diagnostics must not disclose them.
8. Record enough evidence to reproduce the decision: commit and tag, local
   gate, required checks, artifact digests or attestations when available, and
   post-publication smoke results.

## Continuous-delivery rules

Repositories without versioned artifacts treat a squash merge to the protected
default branch as the release boundary. Their playbooks must distinguish
repository validation from operational application. A merge must not silently
restart services, change a workstation, apply firewall policy, publish an
image, or deploy private infrastructure unless an explicitly authorized
workflow owns that action.

## Minimum recovery guidance

Before publication, fix the release branch and rerun its gates. After a merge
but before external delivery, use a new revert or corrective pull request. After
public delivery, fix forward with a new version or image digest; preserve the
original evidence. For operational repositories, document the target-specific
rollback and require explicit operator authorization before applying it.

## Review checklist

- [ ] Release model and authority are unambiguous.
- [ ] Commands exist and match CI.
- [ ] Required checks and branch protection are respected.
- [ ] Changelog or operator notes describe reader-visible impact.
- [ ] Generated artifacts have a named regeneration/check step.
- [ ] Publication permissions and secret boundaries are explicit.
- [ ] Post-release checks cover every delivered surface.
- [ ] Failure paths avoid force-pushing or mutating live systems implicitly.

## CI concurrency

Cancel superseded validation runs using a group unique to the workflow and full
Git ref, with `cancel-in-progress: true`. Full refs distinguish fork PRs and
branches; run IDs prevent superseded runs from sharing a group. For reusable
checks, let the caller own concurrency and avoid duplicating its group in a
called workflow. Scope job-level groups by job when a workflow has several jobs.

Keep release, deployment, and repository-update operations outside cancellable
validation groups. Mixed workflows must isolate PR validation from publication.
After a newer commit supersedes a run, require successful checks on the current
head before merging or delivering; a cancelled older run is not passing evidence.
