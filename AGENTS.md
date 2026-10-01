# ME5305 publication branch guidance

This is the `gh-pages` publication branch. Keep all file changes inside `C:\Repositories\Sites\ME5305`. Other projects are read-only references.

- Maintain Obsidian source notes, editable figures, and full project guidance on `main`.
- Generate HTML with Obsidian's Webpage HTML Export plugin on `main`, staging the complete website in ignored `build/`.
- Track the exported website in `docs/` on this branch. Never ignore `docs/` or commit `build/`, `notes/`, or `figures/` here.
- Fix content and rendering at the source on `main`, then re-export; do not use manual HTML edits as durable fixes.
- Check the current branch and working tree before changes. Preserve unrelated work and ignored local Obsidian state. Save/close Obsidian before switching branches.
- Validate the complete export before synchronizing the contents of `build/` into `docs/`. Check that `docs/index.html` and its assets exist. Remove stale generated files while preserving `docs/.nojekyll` and any intentionally configured `CNAME`.
- Resolve and verify exact paths inside this project before recursive replacements. Avoid repository-wide cleanup, destructive resets, and force pushes.
- Do not merge `main` into this branch to publish. Keep its small root guidance and branch-specific `.gitignore`.
- Publish when requested, and distinguish local preparation from a verified live deployment.

The complete runbook is available with `git show main:PUBLISHING.md`. See [README.md](README.md) for branch status and the release sequence.
