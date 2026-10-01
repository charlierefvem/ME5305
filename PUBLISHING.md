# ME5305 publishing workflow

The instructor's chosen workflow is **Obsidian on `main` → Webpage HTML Export → untracked `build/` → tracked `docs/` on `gh-pages` → GitHub Pages**. This runbook documents setup and releases; creating guidance does not itself create a branch, install a plugin, or deploy the site.

## Branch contract

| Item | `main` | `gh-pages` |
| --- | --- | --- |
| `notes/`, `figures/` | Authoritative publication sources, tracked as populated | Not part of the publication tree |
| `.figure-build/` | Ignored figure-conversion scratch | Ignored; never copy into the website |
| `build/` | Ignored export staging | Ignored export staging; survives normal branch switching |
| `docs/` | Ignored generated output | Tracked complete website |
| Root guidance | Full maintainer guidance | Keep a short branch README and agent instructions explaining the publication contract |

Never copy the `main` ignore file unchanged onto `gh-pages`: its `/docs/` rule would hide the website. Do not force-add around a mistaken ignore rule; correct the branch-specific rule. Do not merge branches to publish.

## Initial vault setup

1. On `main`, open `C:\Repositories\Sites\ME5305\notes` as the Obsidian vault.
2. Add the selected, reviewed content and a useful `index.md` entry point. Keep guidance and import records outside the vault.
3. Install and enable the **Webpage HTML Export** community plugin in this vault when setting up Obsidian. Inspect its current interface and options; no plugin configuration is supplied by this guidance.
4. Set the export destination to **`C:\Repositories\Sites\ME5305\build`**. Export the entry point and explicitly selected student pages with all required media, styles, scripts, and downloads. Check the resulting root is `build/index.html`, not an extra nested vault directory.
5. Add and test needed theme/snippet configuration deliberately. If borrowing ME4305 settings, replace course identity and absolute paths, inspect custom-head script dependencies, and verify each referenced file exists. Do not copy workspace state.
6. Track the vault configuration and supporting files needed to reproduce rendering, after checking their contents. Leave `workspace.json` and `workspace-mobile.json` ignored. Document the exporter version and material settings in the release record.

Frontmatter draft status is not an export exclusion mechanism. Check the selected pages and navigation explicitly. A full release must contain a complete site, not just files changed since the last export.

## First publication branch

Complete an initial `main` commit and produce a validated export before this step. Save/close Obsidian to prevent writes while the vault's tracked files are absent. Inspect `git status --short --branch`, save intended source work, and keep the source commit ID for provenance. Check whether a remote `gh-pages` already exists before creating a new history; local setup observations may be stale.

When no publication branch exists, the recommended initial layout uses an independent history:

```powershell
git switch --orphan gh-pages
```

This removes tracked authoring files from the working tree as part of switching to the empty branch. Run it only after source work is safely committed. Ignored `build/` remains local; verify the export still exists before proceeding. Never use repository-wide cleanup to prepare the branch.

Create a branch-specific `.gitignore` with:

```gitignore
/build/
/.figure-build/
/notes/
/figures/
```

Do **not** ignore `/docs/`. Add a small root README and `AGENTS.md` that tell maintainers to edit sources on `main`, stage the complete export through `build/`, track `docs/`, preserve branch-specific files, and keep all changes inside this project. The full runbook remains available from `main` using `git show main:PUBLISHING.md`.

Create `docs/`, copy the **contents** of the validated export into it, and add an empty `docs/.nojekyll`. Confirm `docs/index.html` exists and all exported assets are present. Review and commit the website and branch-specific files. When publication is requested, push `gh-pages` and configure GitHub **Settings → Pages → Deploy from a branch → `gh-pages` → `/docs`**. GitHub supports `/docs` as a branch publishing source, and `.nojekyll` supports deployment of the prebuilt site. See [GitHub's publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

The expected default project URL from the configured remote is `https://charlierefvem.github.io/ME5305/`. This is an expected address, not evidence that the site is live. Confirm the actual URL in Pages settings, including any custom domain. See [GitHub's project-site URL convention](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

## Routine release

1. **Prepare sources on `main`.** Check branch and working tree, finish content review, verify assets and navigation, and commit the intended source snapshot. For PDF changes, push `main`, wait for the figure Action to pass, and pull its generated SVG commit before exporting. Record its commit ID. Do not carry unrelated tracked modifications across branches.
2. **Export a complete site into `build/`.** Use a full export for releases. An incremental export into an empty staging directory is incomplete; an incremental export into an old directory can retain removed pages. Inspect exporter settings and verify the resulting inventory. Preserve any output still needed before refreshing staging.
3. **Preview the export.** Serve it through a local HTTP preview when possible and test navigation, search if enabled, equations, custom callouts, code, images, downloads, and narrow screens. Check that links and assets will work under the `/ME5305/` project path; origin-root paths such as `/site-lib/...` may resolve outside the project. Check nested pages as well as `index.html`.
4. **Switch branches.** Save/close Obsidian, confirm a clean tracked tree, then use `git switch gh-pages`. The ignored `build/` remains the transfer area. Check the branch and export root again before copying anything.
5. **Synchronize `docs/`.** Treat `build/` as the complete generated-site snapshot. Copy its contents so `build/index.html` becomes `docs/index.html`. Remove stale generated files absent from the new export; a simple overwrite-only copy is insufficient. Preserve intentional branch-managed files such as `.nojekyll` and an existing, configured `CNAME`. If replacing all generated content, recreate an empty `docs/.nojekyll` before committing. Do not introduce a custom domain file speculatively.
6. **Review the publication tree.** Verify `docs/index.html`, generated assets, and `docs/.nojekyll`. Inspect deletions and file counts for an unexpectedly empty or partial export. Preview `docs/` as the final payload, including project-path behavior.
7. **Stage and review.** Use `git add -A -- docs`, then `git diff --cached --stat` and `git diff --cached --check`. Inspect the staged changes, including removed files. If files are unexpectedly missing from staging, use `git check-ignore -v` on the affected paths. Do not stage `build/` or stray vault files.
8. **Commit and publish within the requested scope.** Record the source `main` commit, exporter version, export date, significant settings changes, and verification performed in the release commit message or a branch-root release record. Push `gh-pages` when publication is authorized. Check the Pages deployment result and the actual live pages; a successful local export alone is not a verified deployment.
9. **Return to authoring.** Once publication changes are safely committed and the tree is clean, `git switch main`, then reopen the vault. Confirm the branch before the next edit.

For any scripted recursive replacement, resolve the absolute source and destination and verify they are exactly this project's `build/` and `docs/`. Preview proposed removals and preserve branch-managed files before deleting anything. Do not use a broad `git clean`, destructive reset, or cross-shell deletion pipeline. Staging is ignored for convenience, not protected against deletion.

## Recovery

- For content or rendering fixes, return to `main`, correct the Markdown/assets/configuration, and repeat the export. Hand edits to generated HTML will be lost on the next release.
- To recover a failed export, retain the last known good publication commit and regenerate staging. Do not replace a working site with a partial export.
- To roll back a published release, restore the known-good `docs/` snapshot in a new publication commit and publish it. Preserve branch configuration and history; no force push is needed for a normal rollback.
- If preview, Obsidian export, or live verification cannot be performed, record the limitation and leave the result described at its actual completion stage.
