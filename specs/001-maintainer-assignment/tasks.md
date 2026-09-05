# Maintainer assignment tasks

- [x] Implement metadata-only reusable assignment and reconciliation.
- [x] Verify events, pagination, idempotency, preservation, and failures with API fixtures.
- [x] Pass workflow lint and security checks; review the complete shared change.
- [x] Merge shared workflow and roll out immutable callers through reviewed PRs.
- [x] Verify assignment on actual open items and successful default-branch workflows.
- [x] Record repository coverage, exceptions, merged commits, and cleanup.

## Verification evidence

The shared workflow was merged in PR #13 at
`dca68e2aef0df5caae0e6d03470decd17c7ae1e0`. Ten unit tests, Actionlint,
Zizmor, and the publication scan passed. Manual reconciliation run
[33987460794](https://github.com/bolens/.github/actions/runs/33987460794)
assigned the existing open item #9 to bolens successfully.

All 31 active personal repositories now have reviewed assignment callers. The
three archived repositories remain unchanged. Two empty repositories received a
minimal default branch before their caller changes went through PRs.

All 31 reconciliation jobs completed successfully. The final open-item audit
found no item missing bolens. Existing co-assignees were preserved by the additive
API. Twelve previously unassigned items remained open and were assigned; one
baseline item was closed independently during rollout.

The maintainer-authored draft evidence PR #14 was automatically assigned by
[pull_request_target run 33987590089](https://github.com/bolens/.github/actions/runs/33987590089).
No synthetic issue was created. Issue events, pagination, idempotency, and API
failure cases were covered by the shared regression tests.

Every caller's published file matches its reviewed immutable reference. All
applicable post-merge checks and deployments passed, and the merged caller
branches were removed or already absent. Detailed per-repository commits, run
URLs, scope exceptions, and assignment snapshots are retained in the local fleet
audit report. No product release was required for this automation change.
