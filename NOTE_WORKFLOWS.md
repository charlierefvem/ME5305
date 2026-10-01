# ME5305 note workflows

Use [AGENTS.md](AGENTS.md) for scope and [NOTE_STYLE_GUIDE.md](NOTE_STYLE_GUIDE.md) for editorial conventions. Changes stay inside this repository, including temporary files.

## Revise an existing note

1. Check the current branch and working tree. Author on `main`; preserve unrelated changes.
2. Read the entire note, its source, nearby notes, and any relevant current ME5305 decisions.
3. Identify the note family and student reading path. Distinguish formatting from substantive revision.
4. Preserve technical examples, equations, code, figures, warnings, units, and practical details while making the requested changes.
5. Make uncertainty visible and collect review items. Do not silently correct disputed technical content.
6. Check frontmatter, fence balance, callout boundaries, link targets, asset paths, and exact case.
7. Preview affected rendering when available, review the diff, and report any remaining review or export limitations.

## Convert source material

1. Identify the source version and its status. Use explicit instructor instructions, handwritten notes, annotated slides, digital notes, then historical conversations as the conversion priority.
2. Choose a note family from the reading purpose. Preserve the source filename with a `.md` extension by default unless an existing local convention or explicit instruction requires otherwise.
3. Transcribe technical artifacts and figure annotations faithfully. Use typed code rather than re-OCRing it when available.
4. Turn fragments into readable prose without expanding the scope. Keep examples near the concepts they illustrate.
5. Preserve editable figures and include actual note-facing assets. Missing figures may have clearly marked placeholders in drafts but not in a release.
6. Record provenance and treat the result as a draft. Validate it using the revision checklist above.

## Port an artifact from mechatronics

An import is a deliberate publication copy, not automatic synchronization of the upstream repository.

1. Read the relevant course brief, decisions, source artifact, and any artifact-local README or guidance. Inspect the current file rather than relying on an earlier upload or chat summary.
2. Establish whether the selected file is the accepted source or a proposed revision. `working/generated-drafts/`, `working/note-revisions/`, `working/unpublished-notes/`, and quarantined material are not publishable merely because they are newer. Use instructor direction to resolve a genuinely ambiguous source choice.
3. Compare against any existing local copy. Preserve local fixes and record meaningful differences; do not overwrite with a blind recursive copy.
4. Copy only the selected artifact and the assets/downloads it actually needs into `notes/`. Keep editable figure sources under `figures/` where supplied. Do not import planning records, grading material, obsolete variants, or upstream workspace settings as incidental dependencies.
5. Repair relative links and wiki-links within the imported set. Include any required local dependency or use a verified public destination. Preserve legacy attribution while using ME5305 as the current identity.
6. Record the source and destination mapping outside the vault, using the record below. Include renames and asset mappings so later refreshes can be compared reliably.
7. Review the result in Obsidian and the HTML export when available. Instructor acceptance of the particular content must be established before publication; importing a draft for review is not a release.

For the first import, create `imports/` outside the vault and a descriptive Markdown record there. Include:

- Import date and purpose.
- Upstream project and exact source-relative paths.
- Upstream commit when available and whether selected files had uncommitted changes; for a dirty or unversioned source, record selected-file hashes as well. A commit alone does not identify modified content.
- Source status and the instructor instruction or acceptance on which selection relies.
- Destination paths, including assets and filename changes.
- Publication-specific adaptations and any technical changes requiring upstream follow-up.
- Validation performed and unresolved review items.

Do not modify the upstream source or its tracking files from this project. Report substantive curriculum corrections and their relevant upstream paths to the instructor so they can be reconciled in the development project. On later imports, compare against the recorded source version and local changes instead of treating either copy as automatically newer.

## Update figures and callouts

1. Inspect the editable source and the published asset mapping before replacing a figure.
2. Produce or copy the required web asset inside the vault. Preserve local `assets/` structure for a portable imported collection where useful.
3. Confirm the actual image loads, with meaningful alt text and a concise caption. Preserve handwritten annotations from the source.
4. Before adopting custom callouts, inspect the relevant ME4305 styles and any styles already present locally. Port only needed CSS, enable it deliberately, and verify exported appearance. Do not claim automatic numbering without checking it.
5. Retain ordinary code fences for short snippets and text diagrams; inspect blank lines after quoted callouts and remove duplicated labels.

The PDF-to-SVG Action scans tracked PDFs under `figures/` on every main push and generates matching SVGs under `notes/Images/`. It outlines fonts in disposable copies, validates the whole batch, and commits successful outputs and their manifest. Follow [FIGURE_WORKFLOW.md](FIGURE_WORKFLOW.md); pull the generated commit before Obsidian export. Keep conversion scratch in `.figure-build/`, separate from HTML staging.

## Prepare for publication

1. Confirm the intended student-facing set and update its navigation page.
2. Check links, downloads, asset case, frontmatter visibility, and course identity.
3. Search for draft markers and inspect each hit in context:

   ```powershell
   rg -n 'TODO \(Instructor Review\):|Editorial Note:|Technical Note:|status: draft|Figure Caption|Caption Goes Here' notes
   ```

4. Resolve or exclude unfinished pages and their navigation entries. Check for missing artwork, obsolete ME507 labels, and private or machine-local links.
5. Follow [PUBLISHING.md](PUBLISHING.md) for the complete export and release. Source review alone does not establish that the HTML works.

## Handoff

Summarize what changed, the source/version used for imports, checks actually performed, unresolved instructor-review items, and whether content is only a draft, exported locally, committed for publication, or verified live. Preserve those distinctions.
