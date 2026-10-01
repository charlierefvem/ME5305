# ME5305 website publication

This branch holds the exported website for **ME5305: Mechatronics III**. Author and maintain the Obsidian vault on `main`; use `gh-pages` for the generated publication files.

## Branch layout

- `docs/`: tracked website output, including `.nojekyll`.
- `build/`: ignored local staging for the Obsidian HTML export.
- `notes/` and `figures/`: ignored on this branch; their tracked sources belong to `main`.
- `AGENTS.md` and this README: publication guidance.

## Publication sequence

1. On `main`, finish and commit source changes, then export the complete selected site using **Webpage HTML Export** into `C:\Repositories\Sites\ME5305\build`.
2. Confirm `build/index.html` and all required assets exist and preview the export. Save/close Obsidian before switching branches.
3. Switch to `gh-pages` and synchronize the **contents** of `build/` into `docs/`, removing obsolete generated files while preserving `.nojekyll` and any configured `CNAME`.
4. Check navigation, images, equations, styling, downloads, and paths under `/ME5305/`. Stage with `git add -A -- docs`, inspect the changes, and commit with the source `main` revision and exporter details.
5. When publishing, push `gh-pages` and use GitHub Pages' branch source `gh-pages` with folder `/docs`. Verify the deployment and live site.
6. Return to `main` for further authoring.

Read the full runbook without changing branches:

```powershell
git show main:PUBLISHING.md
```

## Current setup status

The publication branch has been separated from the authoring tree. `docs/.nojekyll` establishes the tracked output directory. No HTML export was present in `build/` when this branch was prepared, so `docs/index.html` and the exported site assets still need to be generated and copied before the first release. GitHub Pages settings and a live deployment have not been verified.

Creating this branch from `main` preserved shared Git history. Removing authoring files here does not remove them from `main`; no history rewrite is needed.
