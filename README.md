## Current source ownership — 2026-10-02

Durable curriculum is now authored in **`D:\Repositories\mechatronics`**, the canonical curriculum repository. Open its `notes/` folder as the note vault and `courses/` as the human-review vault; its root vault is retired. This repository serves student publication/deployment and retains its former source collection as a transition snapshot.

This ownership rule supersedes instructions below or in older runbooks that describe `notes/` or `figures/` as independently maintained sources, recommend opening this vault for authoring, or prescribe a development-to-site editable-copy workflow. Make durable corrections in the master repository, including its shared reference area. Follow that repository's root and course guidance. Do not edit the retained Markdown, figure sources, or vault settings here as parallel curriculum.

The source collection was migrated from `c971962daa47d35cfb36e1546f674a8de2abcd3b` on `main`, with a clean working tree. The master migration record contains exact per-file source hashes, destination paths, and reconciliation evidence. Source draft/review status was preserved.

Existing publication branches, HTML, staging, and conversion tools remain intact. The old export and figure-conversion instructions are transition history; they do not describe an implemented publisher from the new master paths. Preserve the site and source snapshot until Obsidian visual verification and publication continuity checks are complete. Publication automation and redundant-source retirement are later work.

See [CONTENT_OWNERSHIP.md](CONTENT_OWNERSHIP.md) for the current locations and verification limits.

## Historical repository guidance

# ME5305 notes and class resources

This repository maintains the Obsidian notes and web publication for **ME5305: Mechatronics III** at Cal Poly San Luis Obispo. The course emphasizes embedded hardware realization, PCB design, firmware, bring-up, validation, and integrated student projects.

Most curriculum development occurs in `C:\Repositories\mechatronics`. Selected, reviewed artifacts are ported here for student use. `C:\Repositories\Sites\ME4305` supplies the analogous note and publishing conventions. Work in this project changes only files under `C:\Repositories\Sites\ME5305`.

## Repository structure

| Location | Purpose |
| --- | --- |
| `notes/` on `main` | Obsidian vault and student-facing Markdown, images, and downloads |
| `figures/` on `main` | Editable and publication-source figures |
| `.figure-build/` | Ignored conversion tools, intermediates, and diagnostics; never website content |
| `build/` on either branch | Untracked staging for the complete HTML export |
| `docs/` on `gh-pages` | Tracked HTML and assets served by GitHub Pages |
| Root Markdown files on `main` | Maintainer and agent guidance, outside the exported vault |

Open **`notes/`**, rather than the repository root, as the Obsidian vault. Add note-family folders as content arrives; do not populate them with empty instructional stubs.

## Working sequence

1. Develop curriculum in mechatronics and select the reviewed artifact to port.
2. Import and maintain the publication copy in `notes/` on `main`, recording provenance.
3. For PDF figures, push sources under `figures/`, wait for the SVG Action, and pull its generated commit. Then export selected student-facing pages using Webpage HTML Export to `build/`.
4. Preview and validate the complete export.
5. Switch to `gh-pages`, synchronize the export into tracked `docs/`, review, commit, and publish when requested.
6. Return to `main` for further authoring.

See [PUBLISHING.md](PUBLISHING.md) before the first export or branch switch.

## Guidance

- [AGENTS.md](AGENTS.md) establishes repository-wide working rules.
- [COURSE_CONTEXT.md](COURSE_CONTEXT.md) records course scope and authoritative source locations.
- [NOTE_STYLE_GUIDE.md](NOTE_STYLE_GUIDE.md) defines note families and editorial conventions.
- [NOTE_WORKFLOWS.md](NOTE_WORKFLOWS.md) covers conversion, revision, imports, and review.
- [PUBLISHING.md](PUBLISHING.md) documents initial setup and subsequent releases.
- [FIGURE_WORKFLOW.md](FIGURE_WORKFLOW.md) explains automatic PDF-to-SVG conversion and diagnostics.
- [FIGURE_TRIAL.md](FIGURE_TRIAL.md) records the initial validation.

## Setup status

At the guidance baseline on **2026-10-01**, the repository had no commits and only empty `notes/`, `figures/`, and `build/` directories. The configured remote was `https://github.com/charlierefvem/ME5305`; no local or remote-tracking `gh-pages` branch was present. Remote hosting settings were not inspected.

Subsequently, the BLDC notes and vault configuration were imported, and the instructor confirmed that `gh-pages` and the hosted HTML work. PDF figure automation and the initial SVG migration are documented in [FIGURE_WORKFLOW.md](FIGURE_WORKFLOW.md) and [FIGURE_TRIAL.md](FIGURE_TRIAL.md). The original empty-repository observation above is historical.
