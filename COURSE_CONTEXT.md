# ME5305 course context and sources

This is a concise publication-oriented baseline derived from the instructor's request and local sources reviewed on **2026-10-01**. The mechatronics project remains the authority for evolving curriculum decisions. Consult its current files before publishing policy-sensitive or term-specific content.

## Course identity and teaching scope

ME5305 is **Mechatronics III**, the semester successor to legacy **ME507**. The mechatronics sequence is ME3305, ME4305, then ME5305. The source brief lists ME4305 or graduate standing as prerequisites; do not assume all graduate students share the undergraduate sequence.

The audience is fourth- or fifth-year mechanical engineering students, including graduate students, with moderate programming experience, basic circuit familiarity, and little or no PCB design experience. The focus is transforming a conceptual design into working embedded hardware through component selection, schematic design, PCB layout, firmware, bring-up, and integration.

The broad project arc is development hardware, schematic and PCB release, functional board bring-up, and an integrated demonstration. Explain what engineering problem a concept solves before presenting implementation details. Connect design decisions to validation evidence, test access, power and signal constraints, timing, mechanical packaging, and manufacturing risk.

The current brief permits **C or C++**. STM32 microcontrollers and Fusion 360 are common tools, not universal requirements to impose on every example. Build on earlier programming and design ideas while explaining unfamiliar hardware behavior. Do not infer mandatory BLDC projects or broaden ME5305 into a motor-control course.

## Related courses

| Course | Relevant context | Boundary for this repository |
| --- | --- | --- |
| ME3319, System Dynamics | Modeling and numerical analysis of dynamic physical systems; successor to ME322 | Reuse applicable theory with provenance; do not import its lab, MATLAB, or grading rules as ME5305 policy |
| ME4305, Mechatronics II | Integrated mechatronics and embedded implementation; successor to ME405 | Reuse editorial and publishing patterns; its Romi, Python, and frozen-module documentation are course-specific |
| ME5305, Mechatronics III | Hardware realization and project integration; successor to ME507 | Maintain the reviewed student-facing publication here |
| Possible ME5306 | A future systems-integration and estimation concept | Do not describe it as an existing course or required follow-on |

Canvas handles administration and required student actions. GitHub Pages holds durable notes and technical explanations; code repositories distribute software; discussion belongs in the course forum. Do not invent platform links or duplicate changing schedules and policies without a maintained source.

## Source map

Paths below are read-only references for work in this repository.

| Source | Use |
| --- | --- |
| `C:\Repositories\mechatronics\AGENTS.md` | Upstream workflow routing and source authority |
| `C:\Repositories\mechatronics\courses\ME5305\course-brief.md` | Course identity, audience, constraints, and teaching posture |
| `C:\Repositories\mechatronics\courses\ME5305\decisions.md` | Dated decisions and their status; consult before applying older summaries |
| `C:\Repositories\mechatronics\courses\ME5305\open-questions.md` | Unresolved choices, not adopted requirements |
| `C:\Repositories\mechatronics\courses\ME5305\design-guides\` | Existing design-guide source set and local assets |
| `C:\Repositories\mechatronics\courses\ME5305\working\note-revisions\design-guides\README.md` | Draft revision map, instructor-feedback status, and outstanding publication work |
| `C:\Repositories\mechatronics\courses\ME5305\working\` | Drafts, extracted context, and active revision work; not automatically publishable |
| `C:\Repositories\mechatronics\courses\ME5305\future-revisions\` | Deferred observations and proposals; not current policy |
| `C:\Repositories\mechatronics\workflows\lecture-note-conversion.md` | Instructor authorship, source fidelity, and review markers |
| `C:\Repositories\mechatronics\workflows\note-taxonomy-and-linking.md` | Four note families and cross-course reuse |
| `C:\Repositories\mechatronics\courses\ME3319\course-brief.md` | System Dynamics context when relevant to reused material |
| `C:\Repositories\Sites\ME4305\AGENTS.md`, `NOTE_STYLE_GUIDE.md`, and `NOTE_WORKFLOWS.md` | Adapted editorial and vault-maintenance conventions |

The ME4305 `.gitignore`, publication tree, and exporter settings were inspected as examples. Its stored exporter path pointed to a different drive and course. ME5305 has no inherited plugin setup, custom callout styles, frozen-module API workflow, or PDF-to-SVG automation merely because ME4305 has them.

## Import cautions from the baseline review

The design-guide revision set was still marked **Draft for instructor review**. Its README says the eight existing source guides had not been replaced. Detailed technical review, source-coverage audit, renderer preview, and a live Fusion walkthrough remained pending. Its graphics guide referenced pending `assets/me5305-silkscreen-artwork-example.svg` artwork; the legacy ME507 graphic was not the intended final replacement.

Recheck those files when an import is requested. Do not use a newer modification date as evidence of acceptance, import unpublished or quarantined notes, or publish a missing-asset placeholder. The September decisions also narrow Fall 2026 BLDC coverage; older open questions must be interpreted alongside newer decisions.

## Decisions reserved for later work

The two-branch publishing pattern is established by the instructor. Final note filenames, design-guide grouping, custom CSS, figure conversion automation, and exporter options should be settled against actual content and a tested export. Course questions such as the eventual depth of C++, project standardization, and future assessments remain upstream curriculum decisions.
