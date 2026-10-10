# Setup guide

This starter is intended for `Hardikgupta1709/Hardikgupta1709`. It does not include your original README, so merge `README.template.md` into your existing README instead of blindly overwriting your profile.

## macOS commands

```bash
git clone https://github.com/Hardikgupta1709/Hardikgupta1709.git
cd Hardikgupta1709
git switch -c feat/animated-profile-readme
```

Copy the files from this starter ZIP into this cloned folder, preserving the `.github` and `scripts` directories. Then:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python scripts/make_info_card.py
python scripts/fetch_contributions.py
python scripts/render_heatmap_svg.py
```

Optional portrait:

1. Put a photo you are comfortable publishing in the repository root as `source-photo.jpg`.
2. Run:
   ```bash
   python scripts/prep_photo.py source-photo.jpg
   python scripts/make_ascii_svg.py
   ```

Validate generated SVG XML:

```bash
python - <<'PY'
from pathlib import Path
import xml.etree.ElementTree as ET
for name in ("info-card.svg", "contrib-heatmap.svg", "hardik-ascii.svg"):
    path = Path(name)
    if path.exists():
        ET.parse(path)
        print("OK:", name)
    else:
        print("Not generated:", name)
PY
```

Edit `README.md` manually: keep your existing project descriptions, technology badges, social links and contact details. Use the image references shown in `README.template.md`.

Then publish:

```bash
git status
git add README.md scripts data .github/workflows requirements.txt .gitignore   info-card.svg contrib-heatmap.svg hardik-ascii.svg
git commit -m "feat: add animated terminal-style profile"
git push -u origin feat/animated-profile-readme
```

Open a pull request into `main`, review the profile, merge it, and go to GitHub → Actions → Update Profile Art → Run workflow.

## Notes

- GitHub's public contribution HTML markup can change or be rate-limited. The scraper intentionally fails instead of publishing a fabricated blank heatmap.
- The starter workflow uses readable action version tags. For stronger supply-chain security, pin actions to verified full commit SHAs.
- SVG animation support can vary by renderer; the generated images remain readable as static SVGs.
- The workflow updates only the contribution JSON and heatmap SVG, not the README or portrait.
