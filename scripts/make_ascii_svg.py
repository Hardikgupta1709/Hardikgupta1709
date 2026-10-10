#!/usr/bin/env python3
"""Convert prepared-photo.png into a row-by-row animated ASCII SVG."""
from pathlib import Path
import argparse
from PIL import Image
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
CHARS = " .,:;irsXA253hMHGS#9B&@"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default=str(ROOT / "prepared-photo.png"))
    parser.add_argument("--output", default=str(ROOT / "hardik-ascii.svg"))
    parser.add_argument("--columns", type=int, default=72)
    args = parser.parse_args()
    source = Path(args.input)
    if not source.exists():
        raise SystemExit("Missing prepared-photo.png. Run: python scripts/prep_photo.py source-photo.jpg")
    image = Image.open(source).convert("L")
    cols = max(20, args.columns)
    rows = max(1, int(image.height / image.width * cols * 0.52))
    image = image.resize((cols, rows), Image.Resampling.LANCZOS)
    px = list(image.getdata())
    lines = []
    for y in range(rows):
        line = "".join(CHARS[min(len(CHARS)-1, v * len(CHARS) // 256)] for v in px[y*cols:(y+1)*cols])
        lines.append(line.rstrip())
    width, height = cols * 8 + 20, rows * 12 + 24
    rendered = []
    for i, line in enumerate(lines):
        rendered.append(
            '<text x="10" y="%d" class="ascii">%s'
            '<animate attributeName="opacity" values="0;1" dur="1.2s" begin="%.3fs" fill="freeze"/>'
            '</text>' % (18 + i*12, escape(line), i*0.035)
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" role="img">'
        '<title>Animated ASCII portrait</title><desc>Portrait represented with text characters.</desc>'
        '<rect width="100%%" height="100%%" rx="10" fill="#0d1117"/>'
        '<style>.ascii{font-family:ui-monospace,Menlo,monospace;font-size:10px;white-space:pre;fill:#39d353}</style>%s</svg>'
    ) % (width, height, width, height, "".join(rendered))
    Path(args.output).write_text(svg, encoding="utf-8")
    print(f"Generated {args.output}")

if __name__ == "__main__":
    main()
