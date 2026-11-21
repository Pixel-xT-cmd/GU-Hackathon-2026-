"""Download frontend libraries and fonts to vendor them locally in static/vendor."""
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
VENDOR_DIR = BASE_DIR / "static" / "vendor"
FONTS_DIR = VENDOR_DIR / "fonts"
VENDOR_DIR.mkdir(parents=True, exist_ok=True)
FONTS_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def download_file(url, dest_path):
    print(f"Downloading {url} -> {dest_path.name}...")
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as response, open(dest_path, "wb") as out_file:
        out_file.write(response.read())
    print(f"Saved {dest_path.name} ({dest_path.stat().st_size} bytes)")

# Vendor JS
js_files = {
    "htmx.min.js": "https://unpkg.com/htmx.org@1.9.12/dist/htmx.min.js",
    "gsap.min.js": "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js",
    "ScrollTrigger.min.js": "https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"
}

for name, url in js_files.items():
    dest = VENDOR_DIR / name
    if not dest.exists() or dest.stat().st_size == 0:
        try:
            download_file(url, dest)
        except Exception as e:
            print(f"Failed to download {name}: {e}")

# Fonts: Fraunces, Plus Jakarta Sans, Noto Sans Devanagari (woff2 / ttf)
# Use official Google Fonts / github releases
font_files = {
    "Fraunces-SemiBold.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/fraunces/Fraunces%5Bopsz%2Cwght%5D.ttf",
    "PlusJakartaSans-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/plusjakartasans/PlusJakartaSans%5Bwght%5D.ttf",
    "NotoSansDevanagari-Regular.ttf": "https://raw.githubusercontent.com/google/fonts/main/ofl/notosansdevanagari/NotoSansDevanagari%5Bwdth%2Cwght%5D.ttf"
}

for name, url in font_files.items():
    dest = FONTS_DIR / name
    if not dest.exists() or dest.stat().st_size == 0:
        try:
            download_file(url, dest)
        except Exception as e:
            print(f"Failed to download font {name}: {e}")

print("Vendoring complete.")
