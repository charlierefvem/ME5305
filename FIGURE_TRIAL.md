# Initial PDF-to-SVG trial — 2026-10-01

The initial set comprises 28 BLDC PDFs. Each original was moved from `notes/Images/BLDC/` to `figures/BLDC/` without changing its bytes. The matching SVGs are in `notes/Images/BLDC/`; 26 PDF references in four topic notes now reference SVGs. The rotor-animation GIF remains a GIF, with its relative link corrected. Editable upstream artwork and linked LaTeX2AI source files were not modified.

## Local evidence

- Ghostscript 10.07.0 on Windows, upstream-recommended Windows pdf2svg distribution, and pypdf 6.10.0 converted all 28 figures. Exact binary/library identities are recorded by the manifest.
- All 28 outputs retain PDF page bounds, contain no font resources or SVG text, and contain zero raster images.
- Chromium loaded all 28 SVGs as HTML image elements. Source-PDF and SVG renders at 144 dpi had blurred mean RGB errors between 0.3212 and 2.2347 out of 255, below the 3/255 smoke-check threshold. Side-by-side contact sheets were visually reviewed for labels, strokes, clipping, and layout.
- Firefox image-element renders were also checked for `FOC_current_loop`, `hall_and_commutation_and_currents_and_rotor`, `PMSM_model_three_phase`, and `three_phase_inverter_current_example`; errors were approximately 0.7242, 1.2158, 0.3414, and 0.4490 out of 255.
- The local suite passed 15 tests; one test requiring librsvg was skipped because that renderer is supplied by the Linux CI image. Coverage includes unchanged and forced regeneration, changed sources, deleted/edited outputs, pipeline invalidation, malformed/encrypted/multipage input, font checks, collisions, source preservation, crop/rotation/transparency, batch failure, and promotion rollback.

The trial selected PDF 1.4 instead of the planned 1.7 intermediate. Ghostscript 10.07 emitted duplicate dictionary keys inside a compressed object stream for `currents.pdf` at 1.7. Using 1.4 avoids that representation, passes strict PDF inspection, and retains vector transparency. Validation was not weakened.

## GitHub and delivery validation

The actual Linux Action trial is pending at this record's initial creation. Native Windows checks alone do not verify the frozen container or repository push permissions. Record the run result here after the trial.

A fresh Obsidian preview and full Webpage HTML Export using these SVGs remain instructor-side delivery checks. Browser image-element checks passed, but are not a substitute for the actual vault/export integration. No new HTML has been published by this figure task.

The existing PDFs establish compatibility with this source set. A future Illustrator PDF exported without any historical workaround should receive the same visual review; this trial does not claim that every possible Illustrator appearance effect is supported. Separate live-text/WOFF2 experiments in the upstream deferred note remain deferred.
