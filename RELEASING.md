# Release Playbook Standard

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

- whether it publishes versioned releases or continuously delivers `main`;
- the authoritative version source, when one exists;
- the exact local validation command and required GitHub checks;
- which artifacts, packages, images, sites, or configurations are delivered;
- who or what performs publication;
- how to verify the delivered result; and
- how to stop safely and recover from a partial or faulty delivery.

Commands must name real repository entry points. Do not replace a native task
runner with a long list of underlying tools.

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
