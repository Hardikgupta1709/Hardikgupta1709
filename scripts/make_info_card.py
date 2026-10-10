#!/usr/bin/env python3
"""Generate a terminal-style developer card SVG."""
from pathlib import Path
import argparse
from xml.sax.saxutils import escape
import os

ROOT = Path(__file__).resolve().parents[1]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", default=str(ROOT / "info-card.svg"))
    p.add_argument("--name", default=os.getenv("PROFILE_NAME", "hardik@dev"))
    p.add_argument("--role", default=os.getenv("PROFILE_ROLE", "CSE Student / Software Developer"))
    p.add_argument("--focus", default=os.getenv("PROFILE_FOCUS", "Systems Programming, AI/ML"))
    p.add_argument("--languages", default=os.getenv("PROFILE_LANGUAGES", "C, C++, Python"))
    p.add_argument("--building", default=os.getenv("PROFILE_BUILDING", "macMPI"))
    p.add_argument("--status", default=os.getenv("PROFILE_STATUS", "Open to SWE / ML opportunities"))
    a = p.parse_args()
    items = [("USER", a.name), ("ROLE", a.role), ("FOCUS", a.focus),
             ("LANGUAGES", a.languages), ("BUILDING", a.building), ("STATUS", a.status)]
    rows = []
    for i, (key, val) in enumerate(items):
        y = 85 + i*29
        rows.append(
            '<g opacity="1"><text x="28" y="%d" class="key">%s:</text>'
            '<text x="145" y="%d" class="value">%s</text>'
            '<animate attributeName="opacity" values="0;1" dur="0.4s" begin="%.2fs" fill="freeze"/></g>'
            % (y, escape(key), y, escape(val), i*0.16)
        )
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="620" height="280" viewBox="0 0 620 280" role="img">'
        '<title>Developer information</title><desc>Terminal-themed profile card.</desc>'
        '<rect width="620" height="280" rx="12" fill="#0d1117" stroke="#30363d"/>'
        '<rect width="620" height="42" rx="12" fill="#161b22"/><rect y="30" width="620" height="12" fill="#161b22"/>'
        '<circle cx="22" cy="21" r="5" fill="#ff5f56"/><circle cx="40" cy="21" r="5" fill="#ffbd2e"/>'
        '<circle cx="58" cy="21" r="5" fill="#27c93f"/>'
        '<text x="82" y="26" class="heading">hardik@dev — profile</text>'
        '<text x="28" y="64" class="prompt">$ whoami &amp;&amp; neofetch</text>%s'
        '<style>.heading{font:600 14px ui-monospace,monospace;fill:#c9d1d9}'
        '.prompt{font:12px ui-monospace,monospace;fill:#39d353}'
        '.key{font:600 12px ui-monospace,monospace;fill:#79c0ff}'
        '.value{font:12px ui-monospace,monospace;fill:#c9d1d9}</style></svg>'
    ) % "".join(rows)
    Path(a.output).write_text(svg, encoding="utf-8")
    print(f"Generated {a.output}")

if __name__ == "__main__":
    main()
