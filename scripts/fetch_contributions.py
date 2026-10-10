#!/usr/bin/env python3
"""Fetch public GitHub contribution HTML and save date/count JSON."""
from pathlib import Path
from datetime import datetime, timezone
import json, re, requests
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
USERNAME = "Hardikgupta1709"
URL = f"https://github.com/users/{USERNAME}/contributions"
OUTPUT = ROOT / "data" / "contributions.json"

def parse_count(label):
    match = re.search(r"(\d[\d,]*) contribution", label or "", re.I)
    return int(match.group(1).replace(",", "")) if match else 0

def main():
    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 profile-heatmap/1.0"}, timeout=(10, 30))
        r.raise_for_status()
    except requests.RequestException as exc:
        raise SystemExit(f"GitHub request failed: {exc}") from exc
    soup = BeautifulSoup(r.text, "html.parser")
    cells = soup.select("td.ContributionCalendar-day") or soup.select("td[data-date][data-level]")
    days = []
    for cell in cells:
        day = cell.get("data-date")
        if not day:
            continue
        label = cell.get("aria-label") or cell.get("data-aria-label") or ""
        level = cell.get("data-level", "0")
        days.append({"date": day, "count": parse_count(label),
                     "level": int(level) if str(level).isdigit() else 0})
    if len(days) < 300:
        title = soup.title.get_text(" ", strip=True) if soup.title else "unknown"
        raise SystemExit(f"Only found {len(days)} days (page: {title}). GitHub markup may have changed or request was blocked.")
    days.sort(key=lambda x: x["date"])
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {"username": USERNAME, "source": URL,
               "updated_at": datetime.now(timezone.utc).isoformat(), "days": days}
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved {len(days)} days to {OUTPUT}")

if __name__ == "__main__":
    main()
