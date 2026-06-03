#!/usr/bin/env python3
"""Generate simple premium report plates from a JSON spec.

Spec shape:
{
  "title": "Services and Tools Matrix",
  "label": "STACK MATRIX",
  "kicker": "One sentence...",
  "sections": [
    {
      "title": "Local app runtime",
      "color": "#007CBE",
      "cards": [
        {"title": "FastAPI", "body": "Backend API...", "meta": "app/main.py"}
      ]
    }
  ],
  "callout": "Builder move: ..."
}
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH = 2550
HEIGHT = 3300

NAVY = "#08182F"
CYAN = "#11ABE8"
INK = "#0F172A"
SLATE = "#526178"
BORDER = "#D2DEEA"
PALE = "#F5F9FC"
WHITE = "#FFFFFF"


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["Arial Bold.ttf", "Helvetica Bold.ttf"] if bold else ["Arial.ttf", "Helvetica.ttf"]
    roots = ["/System/Library/Fonts/Supplemental", "/Library/Fonts", "/System/Library/Fonts"]
    for root in roots:
        for name in names:
            path = Path(root) / name
            if path.exists():
                return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


FONTS = {
    "eyebrow": load_font(24, True),
    "title": load_font(92, True),
    "h2": load_font(40, True),
    "h3": load_font(32, True),
    "body": load_font(32),
    "small": load_font(27),
    "micro": load_font(18),
}


def wrap(draw: ImageDraw.ImageDraw, text: str, xy: tuple[int, int], width: int, font: ImageFont.ImageFont, fill: str, line: float = 1.2) -> int:
    x, y = xy
    current = ""
    lines: list[str] = []
    for word in text.split():
        test = (current + " " + word).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= width or not current:
            current = test
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    for line_text in lines:
        draw.text((x, y), line_text, font=font, fill=fill)
        y += int(font.size * line)
    return y


def draw_base(spec: dict) -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("RGB", (WIDTH, HEIGHT), PALE)
    draw = ImageDraw.Draw(image)
    draw.rectangle([0, 0, WIDTH, 330], fill=NAVY)
    draw.polygon([(1600, 0), (2140, 0), (1900, 330), (1360, 330)], fill="#10355A")
    draw.rectangle([0, 314, WIDTH, 330], fill=CYAN)
    draw.rounded_rectangle([145, 110, 700, 188], radius=39, fill="#E8F8FF")
    draw.text((185, 135), spec.get("label", "BUILD GUIDE"), font=FONTS["eyebrow"], fill="#007CBE")
    draw.text((1600, 134), spec.get("brand", "Build Guide"), font=FONTS["micro"], fill="#E1EAF5")
    draw.text((145, 430), spec["title"], font=FONTS["title"], fill=NAVY)
    draw.rectangle([145, 560, 680, 578], fill=CYAN)
    wrap(draw, spec.get("kicker", ""), (145, 635), 1900, FONTS["body"], INK)
    return image, draw


def draw_card(draw: ImageDraw.ImageDraw, box: list[int], title: str, body: str, meta: str, color: str) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=34, fill=WHITE, outline=BORDER, width=2)
    draw.rectangle([x1, y1, x1 + 14, y2], fill=color)
    draw.ellipse([x1 + 42, y1 + 45, x1 + 96, y1 + 99], outline=color, width=8)
    draw.text((x1 + 126, y1 + 42), title, font=FONTS["h3"], fill=INK)
    wrap(draw, body, (x1 + 126, y1 + 95), x2 - x1 - 170, FONTS["small"], SLATE)
    if meta:
        draw.rounded_rectangle([x1 + 126, y2 - 85, x2 - 45, y2 - 30], radius=27, fill="#F6FAFD", outline=BORDER, width=1)
        draw.text((x1 + 156, y2 - 68), meta, font=FONTS["micro"], fill=SLATE)


def generate(spec: dict, out_dir: Path) -> Path:
    image, draw = draw_base(spec)
    y = 835
    for section in spec.get("sections", []):
        color = section.get("color", "#007CBE")
        draw.text((145, y), section["title"], font=FONTS["h2"], fill=color)
        y2 = y + 70
        x = 145
        for card in section.get("cards", [])[:3]:
            draw_card(draw, [x, y2, x + 690, y2 + 285], card["title"], card.get("body", ""), card.get("meta", ""), color)
            x += 750
        y += 520
    if spec.get("callout"):
        draw.rounded_rectangle([145, 2915, 2345, 3145], radius=38, fill=NAVY)
        wrap(draw, spec["callout"], (205, 2975), 2050, FONTS["body"], "#E2EEF8")
    out_dir.mkdir(parents=True, exist_ok=True)
    filename = spec.get("filename") or (spec["title"].lower().replace(" ", "-") + ".png")
    path = out_dir / filename
    image.save(path, quality=95)
    return path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("spec", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text())
    print(generate(spec, args.out))


if __name__ == "__main__":
    main()
