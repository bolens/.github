# Maintainer assignment plan

Centralize policy in a reusable workflow in bolens/.github. Each personal repository
has an immutable caller reference and events appropriate to issues and pull requests.
Use pull_request_target for metadata access to fork PRs without a checkout. Grant
only issues:write and pull-requests:write to the assignment job. Restrict execution
to repositories owned by bolens.

Read current item state before event-driven assignment. For schedule and manual runs,
paginate open issues and PRs. Add bolens without replacing other assignees, and verify
the returned assignment. Skip closed or already assigned items.

Use the pinned GitHub Script action. Test its actual inline script with mocked GitHub
API calls, then exercise the published workflow on existing maintainer-owned items.
Validate callers with Actionlint and Zizmor. Roll out only after shared CI and review.
No package release or live operational change is involved.

Constitution checks: minimal shared interface, immutable references, no untrusted code
execution, scoped write permissions, representative caller verification, and no change
to existing reusable workflow interfaces.
