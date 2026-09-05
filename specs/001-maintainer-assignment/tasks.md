# Maintainer assignment tasks

- [x] Implement metadata-only reusable assignment and reconciliation.
- [x] Verify events, pagination, idempotency, preservation, and failures with API fixtures.
- [x] Pass workflow lint and security checks; review the complete shared change.
- [ ] Merge shared workflow and roll out immutable callers through reviewed PRs.
- [ ] Verify assignment on actual open items and successful default-branch workflows.
- [ ] Record repository coverage, exceptions, merged commits, and cleanup.

## Verification evidence

The shared workflow was merged in PR #13 at
`dca68e2aef0df5caae0e6d03470decd17c7ae1e0`. Ten unit tests, Actionlint,
Zizmor, and the publication scan passed. Manual reconciliation run
[33987460794](https://github.com/bolens/.github/actions/runs/33987460794)
assigned the existing open item #9 to bolens successfully.

Fleet caller rollout and its final acceptance checks are still in progress.
