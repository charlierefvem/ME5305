# ME5305 note style guide

Preserve instructor authorship, technical judgment, and the teaching sequence. Notes should support coherent reading and efficient instructor review. Use plain language and nearby examples; avoid adding textbook-length material or empty template sections.

## Note families and layout

| Family | Default location under `notes/` | Purpose |
| --- | --- | --- |
| `topic` | `Topics/` | Lecture-facing narrative in the order students encounter ideas |
| `reference` | `References/` | Standalone definitions, assumptions, methods, derivations, or implementation forms |
| `case-study` | `Case Studies/` | Worked design or implementation journey retaining choices, tradeoffs, and validation |
| `perspective` | `Perspectives/` | Substantial instructor judgment, intuition, misconceptions, or lessons learned |

Create folders when needed. `Images/` is the default for shared note-facing graphics; preserve an imported resource's local `assets/` folder when it keeps its relative links intact. `index.md` will be the student entry point once actual content is available. Resource collections such as design guides may keep a coherent subfolder and navigation page; classify their individual pages by purpose rather than inventing a family for every artifact format.

Topics must remain readable without following every link. References should generally link only to references and keep term, course, assignment, and hardware-specific context in labeled examples. Topics, case studies, and perspectives may link across families where useful. Use `insight` for local observations, not a fifth note family.

## Frontmatter and headings

For new substantive notes, use Obsidian-compatible YAML with `title`, `type`, `tags`, `source`, and `status`. Preserve additional source metadata when importing.

```yaml
---
title: Descriptive Note Title
type: topic
tags:
  - hardware-realization
source:
  course: ME5305
status: draft
---
```

Record detailed file/version provenance in the maintainer import record described in [NOTE_WORKFLOWS.md](NOTE_WORKFLOWS.md). Do not embed workstation paths in student-facing prose. Frontmatter may be displayed by the exporter, so review what it exposes.

Use a frontmatter title and begin content with level-two headings as the initial convention; verify the exported page has a visible title. Preserve imported heading structure until a deliberate adaptation is justified. Use descriptive sections fitted to the material rather than filling a fixed outline.

## Engineering explanations

- Start with the problem, then constraints, a usable model, an example, and the practical consequence as appropriate.
- Define symbols, units, assumptions, coordinate directions, and sign conventions. Preserve equations and derivation order; use LaTeX with `$$` for display math.
- Connect component choices and firmware to physical behavior, measurement, power, timing, debugging, and validation.
- Identify device, board, toolchain, API, and library assumptions when an example depends on them. Use `c` or `cpp` fences as appropriate; do not silently translate languages or substitute hardware.
- State observable checks and limitations when the source supplies them. Do not invent pinouts, voltage limits, ratings, manufacturer capabilities, or lab equipment.
- Use current manufacturer documentation when verifying vendor-specific claims. Separate engineering requirements from practical recommendations and optional refinements.
- Preserve complete technical examples. Reconstruct incomplete code only when the intent is clear and disclose changes affecting behavior or executability.

## Links and assets

Use wiki-links for vault navigation and portable relative Markdown links for assets where practical. Disambiguate duplicate note names. Match filename case exactly and verify both source links and exported destinations; Windows can conceal errors that fail on the published site.

Keep required reading on the current page. Avoid empty reference stubs and broken links to future pages. Do not link student pages to local drives, another vault's filesystem, private Canvas image previews, or upstream working files. Copy the selected asset into this vault and retain provenance.

Store editable figure sources under `figures/` and publication copies inside `notes/`. Tracked PDFs under `figures/` generate SVGs at matching paths under `notes/Images/` through the main-branch Action. Follow [FIGURE_WORKFLOW.md](FIGURE_WORKFLOW.md), preserve editable originals, and review conversions before use. Detailed image alt text should explain meaningful components and relationships; a visible caption should be brief.

## Callouts and code

Adopt ME4305's callout vocabulary where rendering is supported: `note`, `insight`, `algorithm`, `figure`, `table`, `block_listing`, `file_listing`, and `output`. Custom appearance and numbering require compatible CSS; these snippets are **not installed here at the guidance baseline**. Read and port the relevant styles deliberately, then check Obsidian and HTML rendering before depending on custom behavior.

```markdown
> [!note]
> Begin with a normal sentence without repeating the callout label.

> [!insight]
> Use this for a concise conceptual observation or design principle.
```

Use `algorithm` for a procedure or pseudocode whose procedural identity matters. Reserve `block_listing` and `file_listing` for complete implementations or substantial code worth referring to; give each a meaningful description or filename. Short expressions, API calls, syntax fragments, and intermediate steps remain ordinary fenced code. ASCII diagrams remain fenced `text`. Use `output` for console output.

````markdown
> [!file_listing] driver.cpp
> ```cpp
> // A substantial implementation or file excerpt belongs here.
> ```
````

For figures and tables, use a concise caption on one quoted line and a blank line after the complete callout. These examples show syntax only; replace example paths and content with real assets.

```markdown
> [!figure]
> ![Description of the diagram's meaningful components and relationships.](assets/example.svg)
> A short description of the figure.

> [!table]
> A short description of the table.
>
> | Item | Purpose |
> | --- | --- |
> | Example | Explanation |
```

When converting labeled remarks, remove the entire redundant `Note:` or `Insight:` label, including bold markers, and restore sentence capitalization. Formatting-only work must not change the technical content or opportunistically rewrite prose.

## Review status

Use `TODO (Instructor Review):`, `Editorial Note:`, and `Technical Note:` for unresolved draft issues. Collect them at handoff. Before export, resolve or exclude those pages from the publication set; `status: draft` is metadata and must not be assumed to filter exports automatically.
