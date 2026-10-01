# ME5305 repository guidance

These instructions apply throughout this repository. More specific local guidance applies within its directory. Explicit instructor instructions take precedence over project conventions.

## Purpose and scope

Maintain the Obsidian vault and publication copies of notes and class resources for **ME5305, Mechatronics III**, at Cal Poly San Luis Obispo. This project handles student-facing organization, editing, assets, export, and GitHub Pages maintenance.

`C:\Repositories\mechatronics` is the primary curriculum-development project. Read relevant sources there when needed; do not perform curriculum revision there as an incidental part of site maintenance. `C:\Repositories\Sites\ME4305` is an analogous publishing project, not the authority for ME5305 course content.

**Keep all file changes inside `C:\Repositories\Sites\ME5305`.** Other projects are read-only references unless the instructor explicitly changes this boundary. Do not place worktrees, scratch files, exports, or generated artifacts outside this project.

## Read the relevant guidance

- [COURSE_CONTEXT.md](COURSE_CONTEXT.md): course identity, source authority, and upstream source map.
- [NOTE_STYLE_GUIDE.md](NOTE_STYLE_GUIDE.md): note families, Markdown, links, callouts, and technical style.
- [NOTE_WORKFLOWS.md](NOTE_WORKFLOWS.md): editing, source conversion, importing, provenance, and validation.
- [PUBLISHING.md](PUBLISHING.md): branch setup, Obsidian export, staging, release checks, and recovery.

Read the relevant note and source material before editing. Prefer current authoritative files and explicit decisions over old chat summaries. Inspect `git status` and the current branch; preserve unrelated user work.

## Course posture

ME5305 focuses on embedded hardware realization: component selection, schematics, PCB layout, C/C++ firmware, hardware bring-up, validation, and project integration. Teach engineering judgment through realistic constraints, datasheets, observations, and defensible decisions. Firmware is a machine component alongside electronics and mechanics.

Students are senior or graduate mechanical engineers with moderate programming experience, basic circuit familiarity, and little or no PCB experience. Introduce unfamiliar hardware concepts without assuming ME4305's particular robot, Python examples, or firmware API. Connect technical explanations to the engineering problem and next project activity. Do not turn the course into a CAD tutorial, isolated programming course, or advanced motor-control course.

## Authorship and source fidelity

The notes are the instructor's intellectual work. Act as an editor and technical assistant. Preserve voice, teaching sequence, derivations, examples, code, units, sign conventions, and practical judgment. Do not expand notes into textbook chapters or invent course policies, requirements, dates, examples, or technical claims.

For conversion, prioritize explicit instructor instructions, handwritten notes, annotated slides, existing digital notes, then historical conversations. Within a source set, honor the version explicitly identified as current; modification time alone does not make a draft authoritative. Legacy ME507 is historical provenance, not current ME5305 policy.

Flag suspected technical errors rather than silently changing their meaning. Use `TODO (Instructor Review):`, `Editorial Note:`, or `Technical Note:` and report unresolved items. Generated or substantially revised notes remain drafts until instructor review. An instruction approving a particular revision is sufficient; do not repeatedly seek approval for the same work.

## Repository and branch rules

- On `main`, `notes/` is the Obsidian vault; `figures/` holds editable figure sources. Keep maintainer guidance outside the vault.
- `build/` is disposable, untracked export staging on both branches. Never use it for unique source material.
- `docs/` is ignored on `main` and **tracked on `gh-pages`**. HTML is produced by Obsidian's **Webpage HTML Export** community plugin.
- Make note corrections on `main`, then re-export. Do not hand-edit generated HTML as the durable fix or merge the publication tree back into `main`.
- Do not assume `gh-pages`, plugin configuration, custom CSS, figure automation, or a live site exists. Check current state and follow the publishing runbook.
- Preserve `.obsidian/workspace.json` and `workspace-mobile.json` as personal local state; do not edit them unless requested. Routine Obsidian workspace changes are expected.
- Do not bulk-rename notes or assets, import an entire upstream working directory, or copy ME4305 plugin settings verbatim. Preserve established URLs and inspect absolute paths and course-specific configuration.
- Never use broad cleanup such as `git clean -fdx` around the staging workflow. Before any recursive replacement, resolve and verify the exact target under this project and preserve material that cannot be regenerated.

## Completion checks

Validate the changed Markdown, frontmatter, fences, callout boundaries, links, exact filename case, and assets. Preview Obsidian and exported HTML when the task affects rendering and those tools are available. Report what was actually checked and any rendering or publication step still unverified. Review the final diff and summarize unresolved instructor-review items.
