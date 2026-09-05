# Maintainer assignment

Personal repositories assign issues and pull requests to `bolens`. Assignment tracks
responsibility, including the maintainer's own PRs, draft PRs, dependency updates, and
contributions from forks. It does not request a review or remove other assignees.

Each repository's `auto-assign.yml` calls `reusable-auto-assign.yml` at an immutable
commit. Issues trigger on opened, reopened, and transferred events. PRs use opened
and reopened `pull_request_target` events. The reusable job has no checkout and never
executes PR code or evaluates item text. Its token only writes issue and PR metadata.

Daily reconciliation and a manual workflow dispatch assign existing open items that
lack `bolens`, including items created with GITHUB_TOKEN that cannot trigger another
workflow. Closed items and existing assignments are skipped. Removing `bolens` from
an open item is temporary while reconciliation remains enabled.

GitHub documents the relevant [workflow events and token behavior](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows)
and [additive assignment API](https://docs.github.com/en/rest/issues/assignees#add-assignees-to-an-issue).

To change maintainer policy, update and test the shared workflow, merge it, and update
caller pins through reviewed PRs. Do not substitute review requests for assignment:
a sole maintainer cannot review their own PR. Disable the caller workflow to stop
assignment while investigating a failure; repair through a PR. Existing assignments
remain and can be edited manually.
