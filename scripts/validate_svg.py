"""Validate the deliberately small, font-free SVG subset emitted by pdf2svg."""
from __future__ import annotations

import base64
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET

SVG = "http://www.w3.org/2000/svg"
ALLOWED = {
    "svg", "g", "defs", "symbol", "use", "path", "rect", "circle", "ellipse",
    "line", "polyline", "polygon", "clipPath", "mask", "pattern", "image",
    "linearGradient", "radialGradient", "stop", "title", "desc",
}
STYLES = {
    "fill", "fill-opacity", "fill-rule", "stroke", "stroke-width", "stroke-opacity",
    "stroke-linecap", "stroke-linejoin", "stroke-miterlimit", "stroke-dasharray",
    "stroke-dashoffset", "opacity", "clip-path", "clip-rule", "mask",
    "stop-color", "stop-opacity", "color", "display", "visibility",
}


def length_pt(value: str) -> float:
    match = re.fullmatch(r"\s*([0-9.eE+-]+)(pt|px|in|cm|mm)?\s*", value)
    if not match:
        raise ValueError(f"Unsupported SVG dimension: {value!r}")
    number = float(match[1])
    scale = {None: .75, "px": .75, "pt": 1, "in": 72, "cm": 72/2.54, "mm": 72/25.4}
    number *= scale[match[2]]
    if not math.isfinite(number) or number <= 0:
        raise ValueError("SVG dimensions must be finite and positive")
    return number


def validate_svg(path: Path, expected_size=None, source_images: int = 0) -> dict:
    raw = path.read_bytes()
    if re.search(br"<!\s*(DOCTYPE|ENTITY)", raw, re.I):
        raise ValueError("SVG document types and entities are not supported")
    root = ET.fromstring(raw)
    if root.tag != f"{{{SVG}}}svg":
        raise ValueError("Expected an SVG root in the SVG namespace")
    width = length_pt(root.get("width", ""))
    height = length_pt(root.get("height", ""))
    box = [float(n) for n in root.get("viewBox", "").replace(",", " ").split()]
    if len(box) != 4 or not all(map(math.isfinite, box)) or min(box[2:]) <= 0:
        raise ValueError("Invalid SVG viewBox")
    if abs(box[2]/box[3] - width/height) > 1e-5:
        raise ValueError("SVG dimensions and viewBox have different aspect ratios")
    if expected_size and any(abs(a-b) > .05 for a, b in zip((width, height), expected_size)):
        raise ValueError(f"SVG bounds {(width, height)} differ from PDF {expected_size}")
    ids, references = set(), []
    images = paths = 0
    for element in root.iter():
        if not element.tag.startswith(f"{{{SVG}}}") or element.tag.split("}")[-1] not in ALLOWED:
            raise ValueError(f"Unsupported or text-bearing SVG element: {element.tag}")
        tag = element.tag.split("}")[-1]
        paths += tag == "path"
        images += tag == "image"
        for name, value in element.attrib.items():
            attr = name.split("}")[-1]
            if attr.lower().startswith("on") or "font" in attr.lower():
                raise ValueError(f"Active or font-dependent attribute: {attr}")
            if attr == "id":
                if value in ids:
                    raise ValueError(f"Duplicate SVG id: {value}")
                ids.add(value)
            elif attr == "style":
                # Cairo emits simple inline declarations, not arbitrary stylesheets.
                if any(c in value for c in ("\\", "@", "/*", "*/")):
                    raise ValueError("Escaped or indirect CSS is not supported")
                for declaration in value.split(";"):
                    if not declaration.strip():
                        continue
                    prop, separator, _ = declaration.partition(":")
                    if not separator or prop.strip().lower() not in STYLES:
                        raise ValueError(f"Unsupported SVG style: {declaration}")
            elif attr == "href":
                if value.startswith("#"):
                    references.append(value[1:])
                elif tag == "image" and re.fullmatch(r"data:image/(png|jpeg);base64,[A-Za-z0-9+/=\s]+", value):
                    base64.b64decode(re.sub(r"\s", "", value.split(",", 1)[1]), validate=True)
                else:
                    raise ValueError(f"External SVG resource: {value[:100]}")
            if re.search(r"url\s*\(", value, re.I):
                urls = re.findall(r"url\s*\(([^)]*)\)", value, re.I)
                for url in urls:
                    url = url.strip().strip("\"'")
                    if not url.startswith("#"):
                        raise ValueError("Only internal SVG url(#id) resources are allowed")
                    references.append(url[1:])
    if set(references) - ids:
        raise ValueError(f"Unresolved SVG references: {sorted(set(references)-ids)}")
    if images and not source_images:
        raise ValueError("Vector-only PDF unexpectedly became raster SVG content")
    if not paths and not images:
        raise ValueError("SVG has no rendered figure content")
    return {"width_pt": width, "height_pt": height, "paths": paths, "images": images}
