# Maintained source lint

Repositories need blocking lint for their maintained languages, including secondary
scripts. Existing native gates remain authoritative. A repo declares tracked-file
selections and justified exclusions; unknown configuration or empty enabled checks
must fail. Shared tooling uses an immutable ref, read-only permissions, no secrets,
and locked dependencies. It must not execute media, firmware, host configuration,
or deployment operations. Private repositories remain private.

Acceptance: representative valid fixtures pass; deliberate Python, JavaScript,
CSS, Markdown, and shell errors fail. Space/Unicode paths are handled as arguments.
Symlink sources and misspelled config keys fail. Every declared consumer receives
its own scope review and current-head CI evidence. Fish checks every tracked file,
including an invalid second file. Native language/type/build checks remain wired.
