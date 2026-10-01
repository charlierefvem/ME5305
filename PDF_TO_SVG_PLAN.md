# ME5305 PDF to SVG action plan

Status: Implemented design record. See [FIGURE_WORKFLOW.md](FIGURE_WORKFLOW.md) for current operation and [FIGURE_TRIAL.md](FIGURE_TRIAL.md) for actual validation and pending delivery checks. The baseline observations below describe the repository before implementation.

Prepared on 2026-10-01 from the instructor's request, the accepted deferred-work capture, the existing ME4305 action, and the current ME5305 files. All implementation changes are confined to `C:\Repositories\Sites\ME5305`. The other repositories remain read-only.

## Intended outcome

On each push to `main`, identify missing or outdated SVG figures, explicitly outline PDF fonts, convert the resulting PDF to SVG, validate the output, and commit successful generated assets back to `main`. Maintain the existing Obsidian-to-HTML publication process separately; this action neither exports HTML nor writes to `gh-pages`.

The instructor selected this mapping:

```text
figures/BLDC/example.pdf
  -> temporary outlined PDF
  -> notes/Images/BLDC/example.svg
```

Keep the original PDF unchanged. Editable Illustrator documents and linked LaTeX2AI labels remain authoritative in their existing development location. No Illustrator automation or destructive embedding is performed on those originals.

## Findings from the current repositories

- ME4305's action converts new or changed PDFs under `figures/`, also checking for missing SVG counterparts. It mirrors subdirectories into `notes/Images/`, rejects `<text>` and `font-family`, and commits generated SVGs.
- That action invokes `pdf2svg` directly. It has no explicit PDF font-outlining stage and depends on the input already being suitable.
- Its push path filter prevents a scan on unrelated pushes or a push that only deletes an SVG. Changing conversion logic also does not necessarily regenerate existing output.
- ME5305 currently has 28 BLDC PDFs under `notes/Images/BLDC`, one GIF, and no figure inputs under `figures/`. There are 26 lines referencing PDFs in the topic notes.
- Current topic image references use `images/BLDC/...`. The actual directory is `notes/Images/BLDC`; the migration should use the correctly cased, explicit relative path `../Images/BLDC/...` from `notes/Topics/` and verify rendered behavior.
- The upstream Illustrator variant exporter uses Acrobat 5 compatibility and disables Illustrator editability in the exported PDF. It can continue producing PDF intermediates; no second direct-SVG export path is needed for this implementation.

## Conversion choice and the deferred investigation

Use the capture's explicit-outline fallback as the proposed production pipeline: **Ghostscript `pdfwrite` with `-dNoOutputFonts`, then `pdf2svg`**. This matches the instructor's requested improvement to the existing path-based ME4305 action.

Here, outlining means removing font dependencies from a disposable PDF intermediate. It is distinct from flattening PDF transparency. Preserve transparency-capable PDF output; do not force PDF 1.3 or disable transparency to trigger flattening. Those choices can rasterize an entire transparent page. Ghostscript's font-outline option also permits bitmap output for bitmap fonts, so the SVG must be checked for unexpected rasterization. See [Ghostscript's vector-device documentation](https://ghostscript.readthedocs.io/en/latest/VectorDevices.html).

The deferred capture recommends investigating live SVG text first. Preserve that investigation as a bounded feasibility step before declaring a cross-course standard: test an explicitly selected MuPDF/mutool-backed `dvisvgm` with WOFF2 support, inspect embedded fonts, and test actual glyph rendering and copied text in image-embedded SVGs. A successful visual result alone does not establish correct character mappings. The prior Ghostscript-backed experiment did not test this capability. See the [dvisvgm manual](https://dvisvgm.de/Manpage/).

Live-text output is not an automatic alternate mode in the production action. It would conflict with the proposed no-font validation contract and requires its own successful delivery tests and an explicit decision to adopt it. The disposable Illustrator `PlacedItem.embed()` experiment also remains separate; it is not required for unattended GitHub conversion. This plan does not declare either experiment completed or the cross-course capture resolved.

## Repository files to implement

| File | Responsibility |
| --- | --- |
| `.github/workflows/pdf-to-svg.yml` | Trigger, runner/toolchain setup, invocation, diagnostic artifacts, and guarded commit/push |
| `scripts/convert_figures.py` | Discovery, stale-output detection, PDF preprocessing, conversion, and output promotion |
| `scripts/validate_svg.py` | XML, font/resource, geometry, and raster-content validation |
| `figures/svg-manifest.json` | Source-to-output ownership and hashes, conversion fingerprint, and toolchain identity |
| `tests/test_figures.py` | Disposable generated fixtures, nested paths with spaces, and a real BLDC math-label fixture |
| `FIGURE_WORKFLOW.md` | Illustrator PDF handoff, local commands, action behavior, validation, and troubleshooting |

Update the relevant README, agent guidance, and note workflow once implementation is verified. Use the same Python conversion/validation entry points locally and in CI. Keep complex logic out of YAML. Store temporary intermediates and previews in an ignored project-local directory such as `.figure-build/`, without clearing unrelated HTML staging.

## Discovery and freshness

1. Run on every push to `main`, without a path filter, plus manual dispatch with an optional full-regeneration flag. A dispatch on another branch must not write results.
2. Discover tracked PDFs recursively under `figures/`, matching extensions case-insensitively. Exclude test fixtures and intermediate output by location. Sort deterministically and pass filenames as process arguments, never assembled shell text.
3. Mirror each relative PDF path into `notes/Images/` with a `.svg` extension. Detect ambiguous mappings such as `example.pdf` and `example.PDF` before writing; also reject case-only collisions and symlinks escaping the repository.
4. Convert when the output or manifest entry is missing, the source hash changed, the generated file differs from its recorded hash, or the conversion/toolchain fingerprint changed. Do not use file modification times or rely only on the previous push's diff.
5. Treat an existing SVG without recorded ownership as a collision to resolve, rather than silently overwriting potentially hand-authored artwork. On this initial BLDC migration, no existing SVGs occupy the proposed destinations.
6. Report removed/renamed inputs and their old outputs. Initially retain orphaned SVGs for deliberate cleanup with note-link checks; do not automatically delete an asset that may still be referenced.
7. Exit successfully without a commit when there are no candidates or no resulting changes. Regeneration must not alter a timestamp in the manifest on every run.

The manifest identifies both the input bytes and generated bytes, plus a fingerprint of scripts, settings, and the locked toolchain. This lets a later successful run recover from a missed, canceled, or failed earlier run.

## Conversion and validation sequence

For each candidate, work in a separate temporary directory and leave the final output untouched until the entire batch passes.

1. Inspect PDF structure and font resources with pypdf (the implementation selected a single strict parser rather than parsing `pdfinfo`/`pdffonts` output). Require a valid, unencrypted, single-page figure. Reject multi-page inputs with an actionable message instead of silently publishing only page one. Flag unembedded fonts that could trigger machine-dependent substitution.
2. Record page boxes, rotation, and embedded raster content for comparison. Establish the visible-artboard/page-box convention using representative Illustrator exports before fixing the converter settings.
3. Create the outlined intermediate using a command of this form, subject to fixture verification:

   ```bash
   gs -dSAFER -dBATCH -dNOPAUSE \
     -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 \
     -dNoOutputFonts -dAutoRotatePages=/None \
     -dDownsampleColorImages=false \
     -dDownsampleGrayImages=false \
     -dDownsampleMonoImages=false \
     -sOutputFile="$outlined_pdf" -f "$source_pdf"
   pdf2svg "$outlined_pdf" "$candidate_svg"
   ```

   The implementation will use argument arrays. Avoid broad quality presets and automatic rotation. Verify the outlined PDF has no remaining fonts and preserves the selected artboard bounds. `pdf2svg` uses Poppler and Cairo; record their versions as well as the converter version. See the [pdf2svg project](https://github.com/dawbarton/pdf2svg).

4. Parse the SVG as XML. Require an SVG root, finite positive dimensions/viewBox, and valid local fragment references. Reject text-bearing elements (`text`, `tspan`, `textPath`), SVG font elements, font declarations/references, and `foreignObject` in the path-only contract. Inspect CSS as well as XML attributes; do not rely on a case-sensitive text grep alone.
5. Reject external asset dependencies and active scripting. Internal `#id` references are expected; embedded image data is allowed only where justified by source content. Do not ban every `<image>` element because some valid source figures contain raster artwork.
6. Check for unintended whole-page rasterization on vector fixtures, changed bounds, clipped labels, lost glyphs, altered strokes, transforms, and colors. Structural checks alone cannot establish visual fidelity.
7. Promote the batch's validated SVGs and updated manifest together. A failure produces diagnostics and leaves the previous published assets uncommitted and unchanged.

Select and lock the working Ghostscript, pdf2svg, Poppler, Cairo, and validation versions after the fixture trial. Use a reproducible toolchain/container definition rather than treating `ubuntu-latest` plus unversioned package installation as a deterministic environment. Record exact versions in the action summary; regenerate and revalidate when the toolchain changes. Verify repeated builds produce identical SVG bytes with that toolchain before claiming deterministic output.

## GitHub action behavior

- Use a fixed supported Ubuntu runner and the verified locked toolchain. Pin external actions to reviewed commit SHAs at implementation time.
- Give the conversion job `contents: write`, sufficient to commit generated files using the repository's `GITHUB_TOKEN`. Respect branch protection; if direct bot pushes are prohibited, report that and use an agreed pull-request route rather than bypassing protection.
- Serialize runs for this branch. Before pushing, compare the current remote `main` with the source revision used for conversion. If it advanced, restart from the newest revision and recompute candidates with a bounded retry. Never rebase stale generated results onto a newer source PDF or force-push.
- Stage only the generated paths and manifest identified by the successful batch. Do not broadly add all SVGs, source PDFs, note edits, or temporary output.
- Commit only a nonempty validated change set. Use `GITHUB_TOKEN` so the resulting push does not recursively trigger another push workflow; a broad `[skip actions]` marker is unnecessary. See [GitHub's workflow-trigger documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow).
- Produce a summary of scanned, skipped, converted, failed, and orphaned figures. On failure, attach logs, candidate outputs, and comparison previews for diagnosis. A green run means the stated checks passed, not that human visual review occurred.
- Keep source commits and their generated follow-up commits visible. Before exporting the vault locally, pull the generated SVG commit so the HTML exporter sees the current assets.

## Initial BLDC migration

1. Trial representative PDFs without moving sources or changing note links. Include a dense LaTeX2AI-label figure, a circuit diagram, waveform plots, and a composite/clipped figure. Include artificial nested-space and transparency fixtures where the source set lacks them.
2. Generate comparison previews from the original PDFs and the SVGs at matching bounds and resolutions. Review label shape/placement, subscripts, Greek characters, clipping, line weights, transparency, and colors. Establish a tolerant image comparison baseline so antialiasing differences do not mask actual defects or create constant false alarms.
3. Check the selected SVGs as images in Obsidian, in Webpage HTML Export output, and in Chromium and Firefox. Preserve useful Markdown alt text and surrounding explanation: outlined labels are not selectable/searchable text and do not preserve accessible text semantics.
4. Once those checks pass, move the 28 original PDFs to `figures/BLDC` without changing their bytes, generate the full SVG set, and update note image references to the matching `../Images/BLDC/*.svg` paths. Leave `rotor_animation.gif` as a GIF and fix its path if necessary.
5. Land the moved PDFs, generated SVGs, manifest, and updated note links together so no intermediate source commit leaves the vault without its figures. The first action run then verifies or regenerates them as needed.
6. Verify all 28 outputs, every changed link, and a full vault export. Record actual checks and any unverified environment. Update local guidance only after the workflow exists and passes its checks.

## Focused acceptance checks

- First run creates all missing output; a second unchanged run makes no commit.
- A changed PDF regenerates only its output; a deleted SVG is restored on the next main push even if no PDF changed.
- Conversion logic/toolchain changes invalidate the affected output; manual full regeneration also works.
- A missed intermediate push is recovered through source hashes.
- Nested paths, spaces, and uppercase `.PDF` work; ambiguous output paths fail clearly.
- Malformed, encrypted, multi-page, and unsuitable font inputs fail without publishing a partial batch.
- SVG validation catches surviving text/fonts, missing resources, invalid bounds, and unexpected rasterization in vector fixtures.
- Source `.ai`, linked-label PDFs, and input PDFs remain unchanged.
- Concurrent pushes cannot publish SVGs generated from superseded inputs.
- The BLDC comparison set passes visual review in the intended delivery environments before batch adoption.

## Source references and scope

- Deferred record: `C:\Repositories\mechatronics\project\curriculum-revisions\captures\2026-fall\2026-09-29-illustrator-svg-export-workflow.md` (CURR-2026-001).
- Existing action: `C:\Repositories\Sites\ME4305\.github\workflows\pdf-to-svg.yml`.
- Illustrator exporter: `C:\Repositories\mechatronics\courses\ME5305\working\note-revisions\BLDC\figures\export_variants_nested.jsx`.
- ME5305 baseline inspected: commit `8d50eda`.

Implementation is confined to ME5305; ME4305, the upstream capture/exporter, and editable artwork remain unchanged. The intermediate uses PDF 1.4 after the trial exposed a Ghostscript 1.7 object-stream parsing problem; transparency and vector content passed checks. See the trial record for evidence and the unverified Obsidian/export integration. Live-text experiments remain deferred. Results can later inform a shared cross-course standard in the curriculum-development project.
