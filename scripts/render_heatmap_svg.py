#!/usr/bin/env python3
"""Render contributions.json into an animated GitHub-style heatmap SVG."""
from pathlib import Path
from datetime import date
import argparse, json
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
COLORS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", default=str(ROOT / "data" / "contributions.json"))
    p.add_argument("--output", default=str(ROOT / "contrib-heatmap.svg"))
    a = p.parse_args()
    src = Path(a.input)
    if not src.exists():
        raise SystemExit("Missing contributions.json. Run: python scripts/fetch_contributions.py")
    payload = json.loads(src.read_text(encoding="utf-8"))
    days = payload.get("days", [])
    if not days:
        raise SystemExit("No contribution days found; refusing to create a fake/empty heatmap.")
    counts = {x["date"]: max(0, int(x.get("count", 0))) for x in days}
    dates = sorted(counts)
    first, last = date.fromisoformat(dates[0]), date.fromisoformat(dates[-1])
    start = date.fromordinal(first.toordinal() - (first.weekday()+1) % 7)
    end = date.fromordinal(last.toordinal() + (5-last.weekday()) % 7)
    weeks, cur = [], start
    while cur <= end:
        weeks.append([date.fromordinal(cur.toordinal()+d) for d in range(7)])
        cur = date.fromordinal(cur.toordinal()+7)
    positives = sorted(v for v in counts.values() if v > 0)
    thresholds = [positives[min(len(positives)-1, int((len(positives)-1)*q))] for q in (.25,.5,.75)] if positives else [1,1,1]
    def level(n):
        if n <= 0: return 0
        if n <= thresholds[0]: return 1
        if n <= thresholds[1]: return 2
        if n <= thresholds[2]: return 3
        return 4
    cell, gap, margin = 11, 3, 32
    grid_w = len(weeks)*(cell+gap)-gap
    width, height = margin*2+grid_w, 7*(cell+gap)+66
    rects, months, seen = [], [], set()
    for wi, week in enumerate(weeks):
        for d in week:
            if d.day <= 7 and d.month not in seen and d.isoformat() >= dates[0]:
                seen.add(d.month)
                months.append('<text x="%d" y="17" class="month">%s</text>' %
                              (margin+wi*(cell+gap), d.strftime("%b")))
        for di, d in enumerate(week):
            key = d.isoformat()
            if key < dates[0] or key > dates[-1]: continue
            n = counts.get(key, 0)
            x, y = margin+wi*(cell+gap), 28+di*(cell+gap)
            rects.append(
                '<rect x="%d" y="%d" width="%d" height="%d" rx="2" fill="%s" data-date="%s" data-count="%d">'
                '<title>%d contribution(s) on %s</title>'
                '<animate attributeName="opacity" values="0.25;1" dur="0.6s" begin="%.3fs" fill="freeze"/></rect>'
                % (x,y,cell,cell,COLORS[level(n)],key,n,n,key,wi*0.025)
            )
    lx = max(margin, width-150)
    legend = "".join('<rect x="%d" y="%d" width="11" height="11" rx="2" fill="%s"/>' %
                     (lx+i*17,height-20,c) for i,c in enumerate(COLORS))
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%%" viewBox="0 0 %d %d" role="img">'
        '<title>GitHub contributions for %s</title><desc>Daily contribution activity from %s to %s.</desc>'
        '<rect width="100%%" height="100%%" rx="8" fill="#0d1117"/>'
        '<style>.month{font:11px ui-monospace,monospace;fill:#8b949e}.legend{font:10px ui-monospace,monospace;fill:#8b949e}</style>'
        '%s%s<text x="%d" y="%d" class="legend">Less</text>%s<text x="%d" y="%d" class="legend">More</text></svg>'
    ) % (width,height,escape(payload.get("username","")),dates[0],dates[-1],"".join(months),"".join(rects),
         margin,height-11,legend,lx+91,height-11)
    Path(a.output).write_text(svg, encoding="utf-8")
    print(f"Generated {a.output} with {len(counts)} days.")

if __name__ == "__main__":
    main()
