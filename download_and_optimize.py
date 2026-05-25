"""Download images from Drive folder and convert to WebP."""
import json, os, re, sys, time
from pathlib import Path
import requests
from PIL import Image
import pillow_heif

pillow_heif.register_heif_opener()

CRED = Path("/home/n8nstratoma/.google_workspace_mcp/credentials-personal-dani/dani.martprof@gmail.com.json")
RAW = Path(__file__).parent / "assets/raw"
OUT = Path(__file__).parent / "assets/img"
RAW.mkdir(parents=True, exist_ok=True)
OUT.mkdir(parents=True, exist_ok=True)

FILES = [
    ("1Aplh8spC7BoVYCHoroKQU2kdJS0nuw-g", "img-394ae48e.jpg"),
    ("17cbTlaMJBrQ3ci1AN7h8yqTnFup5og7t", "captura-20250718.png"),
    ("14JBL0wxfzFD1nggkgXlYHtsJ7BPeSwbu", "img-1923.jpg"),
    ("1uOHbjcoQBxlb5O3N1VObYuvnEgCN31_H", "img-1924.jpg"),
    ("1bKoyZWYegCNK8Nr5pc4kde6tpphafLa9", "img-1931.jpg"),
    ("1H2BqqzSx-Tflo3YGFAocTwpAa4OBxM9_", "img-1934.jpg"),
    ("1sY2ifItIvrKLDs5qjWBsBuTeXquQhQ2g", "img-1936.jpg"),
    ("10kYNwKlRfXWdrcHdKAZii1sTYXIaFZxS", "img-1939.jpg"),
    ("1zXZ8p6jw9RJVz-XNXxttZTchDI6312lT", "img-1942.jpg"),
    ("1s9P5Vhdf1ulKoEF3aN9rpt8b4vAuGtpl", "img-1943.jpg"),
    ("1bZlSX2ow9vWgvPbb1gHvp4pz0trdd6AL", "img-1946.jpg"),
    ("1-BN0MVYrhNP-7z7Oz0deqNZmeT6JwDwm", "img-1950.jpg"),
    ("18sKc1-E7aDj8NUKYN-XtxDOpk96giRGN", "img-1951.jpg"),
    ("1-CiJN4Hi1KOJXaVV1BdekTKlIOyyEScm", "img-1958.jpg"),
    ("1FRTnvtV7nk_S9T1kVbypWifepebGki58", "img-1959.jpg"),
    ("1yLNTJW6M827_74Qhr39Y5eTVa0GmE3-v", "img-1960.jpg"),
    ("1vZ4RQoG8r-Dwefzm04TR_9M_82HDRELX", "img-1961.jpg"),
    ("12d5QIal7M7DvGNmG0OOd7mzg_aArLz6Y", "img-1962.jpg"),
    ("1dpHgwLzm9_MY5_rNLjzrUapaJsOKh5nA", "img-1967.jpg"),
    ("1VYOyJfS9WSCDj5mCoDUIAniUOYIRLx53", "img-2746.jpg"),
    ("1AWpjbzwcO0ISA0RddTcnh8LEz8fmUjvG", "img-3749.jpg"),
    ("1xJraxROFB_zPDJ-xd6MaSY7bSGB505Br", "img-3751.heic"),
    ("1543zrcftX9jGVNN9i1vdvrzrjvf0okBT", "img-4351.jpg"),
    ("1-FkVWHvYxXLKIlzDh9JxvUSGLP6NW0N0", "img-4549.jpg"),
    ("1N4kHZ0VqEfc-4sR9pnX3TIL4oljQpvIu", "img-4568.jpg"),
]


def get_access_token() -> str:
    c = json.loads(CRED.read_text())
    r = requests.post(c["token_uri"], data={
        "client_id": c["client_id"],
        "client_secret": c["client_secret"],
        "refresh_token": c["refresh_token"],
        "grant_type": "refresh_token",
    }, timeout=30)
    r.raise_for_status()
    return r.json()["access_token"]


def download(file_id: str, dest: Path, token: str) -> None:
    if dest.exists() and dest.stat().st_size > 0:
        return
    url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"
    with requests.get(url, headers={"Authorization": f"Bearer {token}"}, stream=True, timeout=120) as r:
        r.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1 << 16):
                f.write(chunk)


def to_webp(src: Path, stem: str) -> None:
    try:
        img = Image.open(src)
    except Exception as e:
        print(f"  ! cannot open {src.name}: {e}")
        return
    if img.mode in ("RGBA", "LA"):
        img = img.convert("RGB")
    elif img.mode != "RGB":
        img = img.convert("RGB")
    # respect EXIF orientation
    from PIL import ImageOps
    img = ImageOps.exif_transpose(img)

    for width, suffix in [(1600, ""), (640, "-sm")]:
        if img.width <= width:
            resized = img.copy()
        else:
            ratio = width / img.width
            resized = img.resize((width, int(img.height * ratio)), Image.LANCZOS)
        out = OUT / f"{stem}{suffix}.webp"
        resized.save(out, "WEBP", quality=78, method=6)
        print(f"  -> {out.name} ({resized.width}x{resized.height}, {out.stat().st_size//1024} KB)")


def main():
    token = get_access_token()
    for fid, name in FILES:
        dest = RAW / name
        print(f"⬇  {name}")
        download(fid, dest, token)
        stem = Path(name).stem.lower()
        to_webp(dest, stem)
    print("Done.")


if __name__ == "__main__":
    main()
