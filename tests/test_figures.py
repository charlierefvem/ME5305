"""Behavior tests use disposable repositories under this project's ignored .figure-build/."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
import unittest
from unittest.mock import patch

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, FloatObject, NameObject, RectangleObject

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import convert_figures as converter
from validate_svg import validate_svg


def fixture(path, *, pages=1, encrypted=False, rotation=0, crop=False):
    writer = PdfWriter()
    for _ in range(pages):
        page = writer.add_blank_page(width=240, height=120)
        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/ExtGState"): DictionaryObject({
                NameObject("/Alpha"): DictionaryObject({NameObject("/ca"): FloatObject(.5)})})})
        stream = DecodedStreamObject()
        stream.set_data(b"q 1 0 0 rg 15 15 130 70 re f /Alpha gs 0 0 1 rg 90 30 100 70 re f Q\n")
        page[NameObject("/Contents")] = writer._add_object(stream)
        if crop:
            page.cropbox = RectangleObject([10, 10, 230, 110])
        if rotation:
            page.rotate(rotation)
    if encrypted:
        writer.encrypt("private")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as target:
        writer.write(target)


class ConversionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gs = converter.executable(os.getenv("FIGURE_GS"), ["gs", "gswin64c"])
        cls.pdf2svg = converter.executable(os.getenv("FIGURE_PDF2SVG"), ["pdf2svg"])

    def setUp(self):
        work = ROOT / ".figure-build/tests"
        work.mkdir(parents=True, exist_ok=True)
        self.root = work / f"test-{uuid.uuid4().hex}"
        self.root.mkdir()
        subprocess.run(["git", "init", "--quiet", str(self.root)], check=True)
        subprocess.run(["git", "config", "core.autocrlf", "false"], cwd=self.root, check=True)

    def add(self, name="nested folder/A figure.PDF", **kwargs):
        path = self.root / "figures" / name
        fixture(path, **kwargs)
        subprocess.run(["git", "add", "--", path.relative_to(self.root).as_posix()], cwd=self.root, check=True)
        return path

    def convert(self, **kwargs):
        return converter.convert(self.root, gs=self.gs, pdf2svg=self.pdf2svg, **kwargs)

    def test_regeneration_and_unchanged_second_run(self):
        source = self.add()
        original = source.read_bytes()
        first = self.convert()
        self.assertEqual(len(first["converted"]), 1)
        output = self.root / converter.destination(source.relative_to(self.root).as_posix())
        initial_svg = output.read_bytes()
        initial_manifest = (self.root / converter.MANIFEST).read_bytes()
        second = self.convert()
        self.assertEqual(second["changed_paths"], [])
        forced = self.convert(force=True)
        self.assertEqual(forced["changed_paths"], [])
        self.assertEqual(output.read_bytes(), initial_svg)
        self.assertEqual((self.root / converter.MANIFEST).read_bytes(), initial_manifest)
        output.unlink()
        self.assertEqual(len(self.convert()["converted"]), 1)
        output.write_text("broken SVG", encoding="utf-8")
        self.assertEqual(len(self.convert()["converted"]), 1)
        self.assertEqual(source.read_bytes(), original)

    def test_only_changed_input_and_pipeline_invalidation(self):
        first = self.add("first.pdf")
        self.add("second.pdf")
        self.convert()
        fixture(first, crop=True)
        self.assertEqual(self.convert()["converted"], ["figures/first.pdf"])
        with patch.object(converter, "fingerprint", return_value="changed-logic"):
            self.assertEqual(len(self.convert()["converted"]), 2)

    def test_bad_batch_does_not_replace_previous_output(self):
        self.add("good.pdf")
        self.convert()
        before = (self.root / converter.MANIFEST).read_bytes()
        svg_before = (self.root / "notes/Images/good.svg").read_bytes()
        self.add("bad.pdf", pages=2)
        with self.assertRaisesRegex(ValueError, "one PDF page"):
            self.convert(force=True)
        self.assertEqual((self.root / converter.MANIFEST).read_bytes(), before)
        self.assertEqual((self.root / "notes/Images/good.svg").read_bytes(), svg_before)

    def test_encrypted_and_malformed_input(self):
        source = self.add(encrypted=True)
        with self.assertRaisesRegex(ValueError, "Encrypted"):
            self.convert()
        source.write_bytes(b"not a pdf")
        with self.assertRaises(Exception):
            self.convert()
        self.assertFalse((self.root / converter.MANIFEST).exists())

    def test_no_clobber_of_unowned_svg(self):
        self.add("existing.pdf")
        target = self.root / "notes/Images/existing.svg"
        target.parent.mkdir(parents=True)
        target.write_text("hand authored", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "without manifest ownership"):
            self.convert()
        self.assertEqual(target.read_text(), "hand authored")

    def test_removed_source_retains_output(self):
        source = self.add("removed.pdf")
        self.convert()
        subprocess.run(["git", "rm", "-f", "--", "figures/removed.pdf"], cwd=self.root, check=True, capture_output=True)
        report = self.convert()
        self.assertEqual(report["orphans"], ["figures/removed.pdf"])
        self.assertTrue((self.root / "notes/Images/removed.svg").exists())

    def test_rotation_crop_and_transparency_stay_vector(self):
        self.add(rotation=90, crop=True)
        self.convert()
        manifest = json.loads((self.root / converter.MANIFEST).read_text())
        metrics = next(iter(manifest["figures"].values()))["validation"]
        self.assertAlmostEqual(metrics["width_pt"], 100)
        self.assertAlmostEqual(metrics["height_pt"], 220)
        self.assertEqual(metrics["images"], 0)

    @unittest.skipUnless(shutil.which("rsvg-convert"), "librsvg renderer unavailable on this local machine")
    def test_visual_comparison_of_transparency_and_math_labels(self):
        self.add("transparent.pdf", rotation=90, crop=True)
        real = ROOT / "figures/BLDC/FOC_current_loop.pdf"
        if not real.exists():
            real = ROOT / "notes/Images/BLDC/FOC_current_loop.pdf"
        (self.root / "figures/math.pdf").write_bytes(real.read_bytes())
        subprocess.run(["git", "add", "figures/math.pdf"], cwd=self.root, check=True)
        self.assertEqual(len(self.convert(visual_check=True)["converted"]), 2)

    def test_promotion_rolls_back_on_io_failure(self):
        self.add("one.pdf")
        self.add("two.pdf")
        replace = converter.os.replace
        count = 0

        def fail_second(source, target):
            nonlocal count
            count += 1
            if count == 2:
                raise OSError("simulated promotion failure")
            return replace(source, target)

        with patch.object(converter.os, "replace", side_effect=fail_second):
            with self.assertRaisesRegex(OSError, "simulated"):
                self.convert()
        self.assertFalse((self.root / "notes/Images/one.svg").exists())
        self.assertFalse((self.root / converter.MANIFEST).exists())

    def test_case_collision(self):
        self.add("same.pdf")
        # Git's index can represent both names even on a case-insensitive filesystem.
        with patch.object(converter.subprocess, "run", return_value=subprocess.CompletedProcess([], 0, b"figures/same.pdf\0figures/same.PDF\0", b"")):
            with self.assertRaisesRegex(ValueError, "collision"):
                converter.discover(self.root)

    def test_unembedded_font_rejected(self):
        source = self.add()
        writer = PdfWriter(clone_from=source)
        font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                                 NameObject("/Subtype"): NameObject("/Type1"),
                                 NameObject("/BaseFont"): NameObject("/Helvetica")})
        writer.pages[0]["/Resources"][NameObject("/Font")] = DictionaryObject({NameObject("/F1"): font})
        with source.open("wb") as target:
            writer.write(target)
        with self.assertRaisesRegex(ValueError, "Unembedded font"):
            self.convert()

    def test_pdf_with_embedded_math_fonts(self):
        real = ROOT / "figures/BLDC/FOC_current_loop.pdf"
        if not real.exists():
            real = ROOT / "notes/Images/BLDC/FOC_current_loop.pdf"
        source = self.root / "figures/math.pdf"
        source.parent.mkdir()
        source.write_bytes(real.read_bytes())
        subprocess.run(["git", "add", "figures/math.pdf"], cwd=self.root, check=True)
        self.convert()
        metrics = json.loads((self.root / converter.MANIFEST).read_text())["figures"]["figures/math.pdf"]["validation"]
        self.assertGreater(metrics["source_fonts"], 0)
        self.assertEqual(metrics["images"], 0)


class SvgTests(unittest.TestCase):
    def setUp(self):
        work = ROOT / ".figure-build/tests"
        work.mkdir(parents=True, exist_ok=True)
        directory = work / f"svg-{uuid.uuid4().hex}"
        directory.mkdir()
        self.path = directory / "test.svg"

    def svg(self, content, **kwargs):
        self.path.write_text('<svg xmlns="http://www.w3.org/2000/svg" width="72pt" height="36pt" viewBox="0 0 72 36">' + content + '</svg>', encoding="utf-8")
        return validate_svg(self.path, **kwargs)

    def test_rejects_fonts_scripts_resources_and_broken_fragments(self):
        for fragment in ('<text>x</text>', '<tspan>x</tspan>', '<script/>',
                         '<path style="font-family:serif"/>', '<path onload="bad()"/>',
                         '<path style="fill:url(https://example.org/a)"/>',
                         '<use href="#missing"/>', '<image href="file:///x.png"/>',
                         '<path style="f\\ont-family:serif"/>'):
            with self.subTest(fragment=fragment), self.assertRaises(ValueError):
                self.svg(fragment)

    def test_internal_references_and_bounds(self):
        valid = '<defs><path id="p" d="M0 0L10 10"/></defs><use href="#p"/>'
        self.assertEqual(self.svg(valid)["paths"], 1)
        with self.assertRaisesRegex(ValueError, "bounds"):
            self.svg(valid, expected_size=(10, 20))

    def test_unexpected_rasterization(self):
        with self.assertRaisesRegex(ValueError, "raster"):
            self.svg('<image href="data:image/png;base64,YWJj"/>')

    def test_blank_render_fails_visual_comparison(self):
        from PIL import Image
        from check_figure_rendering import compare_pngs
        original, blank = self.path.with_name("original.png"), self.path.with_name("blank.png")
        Image.new("RGB", (50, 50), "black").save(original)
        Image.new("RGB", (50, 50), "white").save(blank)
        with self.assertRaisesRegex(ValueError, "Visual comparison"):
            compare_pngs(original, blank)


if __name__ == "__main__":
    unittest.main()
