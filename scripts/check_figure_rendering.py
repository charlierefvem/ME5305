"""Coarse visual regression check; useful diagnostics, not a substitute for review."""
from pathlib import Path
import subprocess

from PIL import Image, ImageChops, ImageFilter, ImageStat


def compare_pngs(original: Path, rendered: Path, *, limit=3.0) -> dict:
    with Image.open(original) as image:
        first = image.convert("RGB")
    with Image.open(rendered) as image:
        second = image.convert("RGB")
    if first.size != second.size:
        raise ValueError(f"Rendered dimensions differ: {first.size} versus {second.size}")
    # A one-pixel blur at 144 dpi reduces antialiasing noise between renderers.
    difference = ImageChops.difference(first.filter(ImageFilter.GaussianBlur(1)),
                                      second.filter(ImageFilter.GaussianBlur(1)))
    mean = sum(ImageStat.Stat(difference).mean) / 3
    difference.save(rendered.with_name("difference.png"))
    if mean > limit:
        raise ValueError(f"Visual comparison needs review: blurred mean error {mean:.3f}/255 > {limit}/255")
    return {"blurred_mean_error_255": round(mean, 4), "limit_255": limit}


def render_and_compare(pdf: Path, svg: Path, directory: Path) -> dict:
    directory.mkdir(parents=True, exist_ok=True)
    subprocess.run(["pdftoppm", "-cropbox", "-r", "144", "-singlefile", "-png", str(pdf),
                    str(directory / "original")], check=True, capture_output=True, timeout=180)
    original = directory / "original.png"
    with Image.open(original) as image:
        width, height = image.size
    rendered = directory / "rendered.png"
    subprocess.run(["rsvg-convert", "--background-color=white", "--width", str(width),
                    "--height", str(height), "--output", str(rendered), str(svg)],
                   check=True, capture_output=True, timeout=180)
    return compare_pngs(original, rendered)
