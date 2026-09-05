# Maintainer assignment

As the solo maintainer, bolens needs responsibility for issues and pull requests to
be visible across personal repositories, regardless of who opened the item.

## Acceptance

- New, reopened, and transferred issues receive bolens as an assignee.
- New and reopened pull requests receive bolens, including maintainer, bot, and
  external-fork pull requests. Draft status does not change responsibility.
- A scheduled or manual reconciliation covers existing open items and items created
  with GITHUB_TOKEN that do not trigger another workflow.
- Existing co-assignees remain. Already assigned and closed items cause no write.
- Assignment failures remain visible, including an API response that ignores the
  requested assignee. Item titles, bodies, branches, and author names are never code.
- The automation does not request reviews, run PR code, or alter item content.
