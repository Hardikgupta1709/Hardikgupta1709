#!/usr/bin/env python3
"""Crop and prepare a portrait for ASCII conversion."""
from pathlib import Path
import argparse
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

ROOT = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", default=str(ROOT / "source-photo.jpg"))
    parser.add_argument("--output", default=str(ROOT / "prepared-photo.png"))
    parser.add_argument("--width", type=int, default=100)
    args = parser.parse_args()
    source = Path(args.input)
    if not source.exists():
        raise SystemExit(f"Photo not found: {source}. Put one at {ROOT / 'source-photo.jpg'} or pass a path.")
    image = Image.open(source).convert("RGB")
    ratio = 4 / 5
    w, h = image.size
    if w / h > ratio:
        nw = int(h * ratio)
        left = (w - nw) // 2
        image = image.crop((left, 0, left + nw, h))
    else:
        nh = int(w / ratio)
        top = (h - nh) // 2
        image = image.crop((0, top, w, top + nh))
    image = image.resize((args.width, int(args.width * 1.25)), Image.Resampling.LANCZOS)
    image = ImageOps.autocontrast(ImageOps.grayscale(image))
    image = ImageEnhance.Contrast(image).enhance(1.25).filter(ImageFilter.SHARPEN)
    image.save(args.output)
    print(f"Prepared image: {args.output}")

if __name__ == "__main__":
    main()
