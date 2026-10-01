# PDF figures for the ME5305 vault

Export an ordinary, single-page PDF from the editable Illustrator artwork, with its fonts embedded. Keep the `.ai` file and linked LaTeX2AI labels editable in their development location. No transparent-pixel object, manual outlining, or destructive embedding workaround is required for this pipeline. The automation outlines fonts in a disposable PDF copy, then creates a self-contained SVG.

## Authoring and publication

1. On `main`, place the selected figure PDF under `figures/`, preserving its intended subfolders. For example, `figures/BLDC/FOC_current_loop.pdf` produces `notes/Images/BLDC/FOC_current_loop.svg`.
2. Commit and push the PDF. **Convert PDF figures to SVG** checks every push to `main`, including pushes that only remove or damage an SVG. It scans tracked PDFs, compares content and toolchain hashes, and generates missing or stale outputs.
3. Wait for a successful Action run, then pull its generated commit before editing further or exporting HTML. Review changed figures. A successful automated check does not replace review of mathematical meaning or small labels.
4. Reference the SVG with an exact-case relative path, such as `../Images/BLDC/FOC_current_loop.svg` from a topic note. Preserve meaningful alt text and surrounding explanations: outlined labels have no selectable or searchable text semantics.
5. Export the vault through Webpage HTML Export and follow [PUBLISHING.md](PUBLISHING.md). The figure Action does not export HTML or publish `gh-pages`.

For a new figure, let the Action create its SVG before adding the note link, or generate it locally and commit the source, output, manifest, and link together. Ordinary new PDFs should not have an existing hand-authored SVG at the destination; the converter refuses to overwrite an output it does not own.

## Conversion and checks

The same Python entry point runs locally and in CI. Ghostscript `pdfwrite` uses `-dNoOutputFonts` and PDF 1.4, preserving transparency while avoiding compressed object streams. `pdf2svg` converts that outlined copy. Sources are never rewritten. This is font outlining, not whole-page rasterization or forced transparency flattening.

Inputs must be unencrypted, single-page PDFs with embedded fonts. Unembedded fonts, Type3 fonts, unsupported page units, and ambiguous filenames fail for review. Checks cover page bounds, remaining fonts, SVG text, external resources, scripting, broken internal references, and unexpected rasterization of vector-only inputs. In CI, Poppler renders the original PDF and librsvg renders the SVG at 144 dpi. A one-pixel blur accommodates antialiasing; mean RGB difference above 3/255 fails. This coarse check can miss small local defects and does not establish accessibility or pedagogical correctness.

All candidates must pass before any output is promoted. Failures retain the previous output batch. `figures/svg-manifest.json` records source/output hashes, converter fingerprint, toolchain identity, and validation results. Do not hand-edit generated SVGs or the manifest to bypass a failure. Removed sources are reported as orphans; their outputs remain until deliberate link review and cleanup.

CI uses the digest-pinned Debian image and dated package snapshot in `scripts/figure-toolchain/Dockerfile`, plus hashed Python requirements. Updating those pins is a deliberate toolchain change requiring regression review. Native Windows results can differ from Linux; CI regenerates them once and records the production toolchain. Repeated runs with the same source and toolchain should produce no change.

## Running and diagnosing

GitHub's Actions page supports a manual run on `main`; enable **force** to regenerate every figure. The workflow needs permission to push generated commits to `main`. It uses the repository's `GITHUB_TOKEN`; those bot pushes do not recursively trigger this push workflow. Branch rules that forbid its push must be resolved by the maintainer rather than bypassed with force pushes. Racing source pushes cause a fresh conversion from current `main`, with up to three attempts.

For a native local run, install or provide Python 3.11+, the pinned pypdf dependency, Ghostscript, and pdf2svg. Keep project-specific downloads and temporary files inside this project. Run from the repository root:

```powershell
python -B scripts/convert_figures.py --gs "path/to/gswin64c.exe" --pdf2svg "path/to/pdf2svg.exe"
python -B -m unittest discover -s tests -v
```

Tests accept `FIGURE_GS` and `FIGURE_PDF2SVG` environment variables. `--include-untracked` explicitly includes new source PDFs for an initial local migration; normally stage PDFs first. `--visual-check` additionally needs Pillow, Poppler's `pdftoppm`, and `rsvg-convert`. The CI image supplies all of these and runs the full tests before conversion. The CI orchestration and publication scripts are restricted to GitHub Actions on `main`.

Disposable intermediates, diagnostics, local tools, and test repositories live in **`.figure-build/`**, which is ignored and separate from HTML staging in `build/`. The current report is `.figure-build/report.json`. Failed Actions upload diagnostic artifacts for seven days. Inspect the first error and comparison previews; fix the source or conversion logic, then rerun. Never copy `.figure-build/` to `docs/`. Keep it ignored on both branches and in the local Git exclude file when transitioning an older publication branch.

See [FIGURE_TRIAL.md](FIGURE_TRIAL.md) for the initial BLDC evidence and remaining delivery checks, and [PDF_TO_SVG_PLAN.md](PDF_TO_SVG_PLAN.md) for the design record.
