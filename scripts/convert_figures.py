"""Outline disposable PDF copies and publish validated SVG batches.

No shell interpolation, source modification, or automatic deletion of orphaned SVGs.
Requires Python 3.11+, pypdf, Ghostscript, and pdf2svg.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import uuid

import pypdf
from pypdf import PdfReader
from validate_svg import validate_svg

REPOSITORY = Path(__file__).resolve().parents[1]
MANIFEST = "figures/svg-manifest.json"
GS_OPTIONS = [
    "-dSAFER", "-dBATCH", "-dNOPAUSE", "-sDEVICE=pdfwrite",
    # PDF 1.4 retains transparency without PDF 1.5+ compressed object streams.
    # GS 10.07 emitted duplicate keys in an unused object-stream dictionary for
    # currents.pdf; 1.4 avoids that parser ambiguity without rasterizing it.
    "-dCompatibilityLevel=1.4", "-dNoOutputFonts", "-dAutoRotatePages=/None",
    "-dUseCropBox", "-dDownsampleColorImages=false",
    "-dDownsampleGrayImages=false", "-dDownsampleMonoImages=false",
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def json_bytes(value) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def inside(root: Path, relative: str | Path) -> Path:
    path = root / relative
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes project: {relative}")
    # Do not let a symlink redirect publication writes, even within the project.
    for item in (path, *path.parents):
        if item == root:
            break
        if item.is_symlink():
            raise ValueError(f"Symlink is not an allowed figure path: {relative}")
    return path


def run(args, *, cwd: Path, env=None) -> str:
    result = subprocess.run([str(a) for a in args], cwd=cwd, env=env,
                            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
    output = result.stdout + result.stderr
    if result.returncode:
        raise RuntimeError(f"Command failed ({result.returncode}): {args[0]}\n{output}")
    return output


def inspect_pdf(path: Path, *, outlined=False) -> dict:
    reader = PdfReader(path, strict=True)
    if reader.is_encrypted:
        raise ValueError(f"Encrypted PDF is not a figure input: {path.name}")
    if len(reader.pages) != 1:
        raise ValueError(f"Expected one PDF page, found {len(reader.pages)}: {path.name}")
    page = reader.pages[0]
    width, height = float(page.cropbox.width), float(page.cropbox.height)
    rotation = int(page.get("/Rotate", 0)) % 360
    if rotation not in (0, 90, 180, 270):
        raise ValueError("PDF rotation must be a multiple of 90 degrees")
    if rotation in (90, 270):
        width, height = height, width
    if any(not math.isfinite(n) or n <= 0 for n in (width, height)):
        raise ValueError("PDF has invalid page bounds")
    if float(page.get("/UserUnit", 1)) != 1:
        raise ValueError("Non-default PDF UserUnit is not supported")
    fonts, images, visited = set(), set(), set()

    def walk(resources):
        if not resources:
            return
        resources = resources.get_object()
        identity = id(resources)
        if identity in visited:
            return
        visited.add(identity)
        for ref in resources.get("/Font", {}).get_object().values() if "/Font" in resources else []:
            font = ref.get_object()
            fonts.add(str(font.get("/BaseFont", font.get("/Subtype", "unknown"))))
            if outlined:
                raise ValueError("Outlined PDF still contains font resources")
            descendants = font.get("/DescendantFonts", [font])
            for descendant in descendants:
                descendant = descendant.get_object()
                descriptor = descendant.get("/FontDescriptor")
                if descendant.get("/Subtype") == "/Type3":
                    raise ValueError("Type3 fonts require a separate raster/vector review")
                if descriptor is None or not any(key in descriptor.get_object() for key in ("/FontFile", "/FontFile2", "/FontFile3")):
                    raise ValueError(f"Unembedded font could require substitution: {font.get('/BaseFont')}")
        xobjects = resources.get("/XObject")
        if xobjects:
            for ref in xobjects.get_object().values():
                obj = ref.get_object()
                if obj.get("/Subtype") == "/Image":
                    images.add(id(obj))
                walk(obj.get("/Resources"))
        patterns = resources.get("/Pattern")
        if patterns:
            for ref in patterns.get_object().values():
                walk(ref.get_object().get("/Resources"))
        states = resources.get("/ExtGState")
        if states:
            for ref in states.get_object().values():
                mask = ref.get_object().get("/SMask")
                if mask and hasattr(mask.get_object(), "get"):
                    group = mask.get_object().get("/G")
                    if group:
                        walk(group.get_object().get("/Resources"))

    walk(page.get("/Resources"))
    # page.images also discovers inline images, not only XObject resources.
    image_count = max(len(images), len(page.images))
    return {"size_pt": [width, height], "fonts": sorted(fonts), "images": image_count}


def toolchain(gs: str, pdf2svg: str) -> dict:
    identity = {"system": platform.system(), "machine": platform.machine(),
                "pypdf": pypdf.__version__, "ghostscript": run([gs, "--version"], cwd=REPOSITORY).strip(),
                "gs_binary": digest(Path(gs)), "pdf2svg_binary": digest(Path(pdf2svg))}
    dlls = sorted(Path(pdf2svg).parent.glob("*.dll")) if os.name == "nt" else []
    if dlls:
        identity["pdf2svg_libraries"] = {p.name: digest(p) for p in dlls}
    if sys.platform.startswith("linux"):
        identity["packages"] = run(["dpkg-query", "-W", "-f=${Package}=${Version}\n",
                                    "ghostscript", "pdf2svg", "libcairo2", "libpoppler-glib8", "libpoppler126",
                                    "librsvg2-bin", "python3-pil"], cwd=REPOSITORY).strip()
    return identity


def fingerprint(identity: dict, visual_check=False) -> str:
    scripts = {p: digest(REPOSITORY / "scripts" / p) for p in
               ("convert_figures.py", "validate_svg.py", "check_figure_rendering.py")}
    return hashlib.sha256(json_bytes({"toolchain": identity, "scripts": scripts, "options": GS_OPTIONS,
                                     "visual_check": visual_check})).hexdigest()


def discover(root: Path, include_untracked=False) -> list[str]:
    args = ["git", "ls-files", "-z", "--cached"]
    if include_untracked:
        args += ["--others", "--exclude-standard"]
    args += ["--", "figures"]
    result = subprocess.run(args, cwd=root, check=True, capture_output=True)
    paths = sorted(set(p for p in result.stdout.decode("utf-8").split("\0") if p and p.lower().endswith(".pdf")))
    outputs = {}
    existing = {p.relative_to(root).as_posix().casefold(): p.relative_to(root).as_posix()
                for p in (root / "notes/Images").rglob("*") if p.is_file()}
    for path in paths:
        output = destination(path)
        folded = output.casefold()
        if folded in outputs:
            raise ValueError(f"Output collision: {path} and {outputs[folded]}")
        if folded in existing and existing[folded] != output:
            raise ValueError(f"Output has a case-only collision: {output}")
        outputs[folded] = path
    # Check the entire index for collisions before touching the filesystem.
    # On Linux, an uppercase index-only fixture can sort before the real file;
    # on Windows both spellings resolve to the same file.
    for path in paths:
        if not inside(root, path).is_file():
            raise ValueError(f"Tracked PDF is missing; stage its intended removal first: {path}")
        inside(root, destination(path))
    return paths


def destination(source: str) -> str:
    return (Path("notes/Images") / Path(source).relative_to("figures").with_suffix(".svg")).as_posix()


def convert_one(source: Path, candidate: Path, gs: str, pdf2svg: str) -> dict:
    before = inspect_pdf(source)
    candidate.parent.mkdir(parents=True, exist_ok=True)
    intermediate = candidate.with_suffix(".outlined.pdf")
    environment = os.environ.copy()
    environment.update(TEMP=str(candidate.parent), TMP=str(candidate.parent), TMPDIR=str(candidate.parent))
    log = run([gs, *GS_OPTIONS, f"-sOutputFile={intermediate}", "-f", source], cwd=candidate.parent, env=environment)
    candidate.with_suffix(".gs.log").write_text(log, encoding="utf-8")
    if re_search_substitution(log):
        raise ValueError("Ghostscript reported a font substitution or missing glyph; inspect its log")
    after = inspect_pdf(intermediate, outlined=True)
    if any(abs(a-b) > .05 for a, b in zip(before["size_pt"], after["size_pt"])):
        raise ValueError("Ghostscript changed the visible PDF page dimensions")
    if after["images"] and not before["images"]:
        raise ValueError("Ghostscript rasterized a vector-only PDF")
    log = run([pdf2svg, intermediate, candidate], cwd=candidate.parent, env=environment)
    candidate.with_suffix(".pdf2svg.log").write_text(log, encoding="utf-8")
    result = validate_svg(candidate, expected_size=before["size_pt"], source_images=before["images"])
    result["source_fonts"] = len(before["fonts"])
    result["source_images"] = before["images"]
    return result


def re_search_substitution(log: str) -> bool:
    import re
    return bool(re.search(r"substitut|can't find.*font|cannot find.*font|missing glyph", log, re.I))


def convert(root: Path, *, gs: str, pdf2svg: str, force=False, include_untracked=False, visual_check=False) -> dict:
    root = root.resolve()
    work = inside(root, ".figure-build/runs")
    work.mkdir(parents=True, exist_ok=True)
    batch = work / f"batch-{uuid.uuid4().hex}"
    batch.mkdir()
    report = {"scanned": 0, "converted": [], "skipped": [], "orphans": [], "changed_paths": [], "status": "failed"}
    report_path = inside(root, ".figure-build/report.json")
    try:
        manifest_path = inside(root, MANIFEST)
        previous = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"schema": 1, "figures": {}}
        if previous.get("schema") != 1 or not isinstance(previous.get("figures"), dict):
            raise ValueError("Unsupported SVG manifest schema")
        entries = dict(previous["figures"])
        sources = discover(root, include_untracked)
        report["scanned"] = len(sources)
        report["orphans"] = sorted(set(entries) - set(sources))
        identity = toolchain(gs, pdf2svg)
        signature = fingerprint(identity, visual_check)
        report["toolchain"] = identity
        candidates = []
        for source in sources:
            output = destination(source)
            target = inside(root, output)
            old = entries.get(source)
            if target.exists() and (not old or old.get("output") != output):
                raise ValueError(f"Refusing to overwrite SVG without manifest ownership: {output}")
            source_hash = digest(inside(root, source))
            if (not force and old and target.exists() and old.get("source_sha256") == source_hash
                    and old.get("pipeline_sha256") == signature and old.get("output_sha256") == digest(target)):
                report["skipped"].append(source)
                continue
            candidate = batch / output
            metrics = convert_one(inside(root, source), candidate, gs, pdf2svg)
            if visual_check:
                from check_figure_rendering import render_and_compare
                metrics["visual"] = render_and_compare(inside(root, source), candidate,
                                                       candidate.parent / (candidate.stem + "-preview"))
            entries[source] = {"output": output, "source_sha256": source_hash,
                               "output_sha256": digest(candidate), "pipeline_sha256": signature,
                               "toolchain": identity, "validation": metrics}
            candidates.append((candidate, target))
            report["converted"].append(source)
            print(f"Converted {source} -> {output}", flush=True)
        # Recheck inputs immediately before publishing this batch.
        for source in sources:
            if digest(inside(root, source)) != entries[source]["source_sha256"]:
                raise ValueError(f"Source changed during conversion: {source}")
        next_bytes = json_bytes({"schema": 1, "figures": entries})
        staged_manifest = batch / "manifest.json"
        staged_manifest.write_bytes(next_bytes)
        if entries or manifest_path.exists():
            candidates.append((staged_manifest, manifest_path))
        # Roll back any promoted files if an I/O error interrupts promotion.
        backups = []
        try:
            for candidate, target in candidates:
                if target.exists() and target.read_bytes() == candidate.read_bytes():
                    continue
                original = target.read_bytes() if target.exists() else None
                target.parent.mkdir(parents=True, exist_ok=True)
                backups.append((target, original))
                os.replace(candidate, target)
                report["changed_paths"].append(target.relative_to(root).as_posix())
        except Exception:
            for target, original in reversed(backups):
                if original is None:
                    target.unlink(missing_ok=True)
                else:
                    target.write_bytes(original)
            report["changed_paths"] = []
            raise
        report["status"] = "passed"
        return report
    except Exception as error:
        report["error"] = str(error)
        raise
    finally:
        report_path.write_bytes(json_bytes(report))


def executable(value: str | None, choices: list[str]) -> str:
    for candidate in ([value] if value else choices):
        located = shutil.which(candidate)
        if located:
            return str(Path(located).resolve())
    raise ValueError(f"Required executable missing: {value or ', '.join(choices)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=REPOSITORY)
    parser.add_argument("--gs")
    parser.add_argument("--pdf2svg")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--visual-check", action="store_true", help="Compare Poppler and librsvg renders; requires Pillow and rsvg-convert")
    parser.add_argument("--include-untracked", action="store_true", help="Explicit opt-in for an initial local migration")
    args = parser.parse_args()
    report = convert(args.root, gs=executable(args.gs, ["gs", "gswin64c"]),
                     pdf2svg=executable(args.pdf2svg, ["pdf2svg"]), force=args.force,
                     include_untracked=args.include_untracked, visual_check=args.visual_check)
    print(f"Scanned {report['scanned']}; converted {len(report['converted'])}; skipped {len(report['skipped'])}; orphans {len(report['orphans'])}")
    for path in report["orphans"]:
        print(f"REVIEW retained orphan: {path}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as error:
        print(f"Figure conversion failed: {error}", file=sys.stderr)
        sys.exit(1)
