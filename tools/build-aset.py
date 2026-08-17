# Membangun aset gambar situs CARVA dari company profile PDF.
import os, shutil
import pymupdf
from PIL import Image

SCRATCH = r"C:\temp\claude\D--Kerjaan-ayah--proyek-saya-simrhl\92923f66-3096-486f-b5bb-3acb3b2849b8\scratchpad"
SRC = os.path.join(SCRATCH, "carva_assets")
IDX = os.path.join(SCRATCH, "sheets", "index.txt")
PDF = r"D:\Desktop\@arsip\web carva\2026. COMPRO CARVA - 15082026.pdf"
DEST = r"D:\Kerjaan\ayah\@proyek_saya\web_carva\assets\img"

for sub in ("", "org", "galeri", "galeri/th"):
    os.makedirs(os.path.join(DEST, sub), exist_ok=True)

num2file = {}
with open(IDX, encoding="utf8") as fh:
    for line in fh:
        n, name = line.rstrip("\n").split("\t")
        num2file[int(n)] = os.path.join(SRC, name)


def load(n):
    return Image.open(num2file[n])


def save_webp(im, out, maxw, q=80, alpha=False):
    im = im.copy()
    if alpha:
        im = im.convert("RGBA")
    else:
        im = im.convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(os.path.join(DEST, out), "WEBP", quality=q, method=6)
    return os.path.getsize(os.path.join(DEST, out))


def trim_alpha(im):
    im = im.convert("RGBA")
    bb = im.getchannel("A").getbbox()
    return im.crop(bb) if bb else im


log = []

# --- logo (PNG, transparansi) ---------------------------------------------
logo = trim_alpha(load(81))          # 800x538 "carva abhinaya carva utama"
logo.save(os.path.join(DEST, "logo-carva-dari-pdf.png"), optimize=True)
log.append(("logo-carva-dari-pdf.png", logo.size))

# versi putih untuk footer gelap: semua piksel non-transparan -> putih
w = logo.copy()
px = w.load()
for y in range(w.height):
    for x in range(w.width):
        r, g, b, a = px[x, y]
        if a > 0:
            px[x, y] = (255, 255, 255, a)
w.save(os.path.join(DEST, "logo-carva-putih.png"), optimize=True)
log.append(("logo-carva-putih.png", w.size))

# favicon: pakai logo penuh di atas kanvas persegi transparan
side = max(logo.size)
fav = Image.new("RGBA", (side, side), (0, 0, 0, 0))
fav.paste(logo, ((side - logo.width) // 2, (side - logo.height) // 2))
fav.resize((180, 180), Image.LANCZOS).save(os.path.join(DEST, "favicon-dari-pdf.png"), optimize=True)
log.append(("favicon-dari-pdf.png", (180, 180)))

# --- gambar utama ----------------------------------------------------------
plain = [
    (3,  "hero-hutan.webp",      1400, 82),
    (79, "hutan-pinus.webp",     1600, 80),
    (6,  "tim-lapangan.webp",    1229, 82),
    (19, "jasa-kehutanan.webp",  1000, 82),
    (20, "jasa-lingkungan.webp", 1000, 82),
    (21, "jasa-manajemen.webp",  1000, 82),
    (12, "iso-9001.webp",         700, 85),
    (13, "iso-45001.webp",        700, 85),
    (86, "planet-hijau.webp",    1000, 82),
]
for n, out, mw, q in plain:
    log.append((out, save_webp(load(n), out, mw, q)))

# dengan transparansi
for n, out, mw in [(2, "globe-lumut.webp", 900), (5, "daun.webp", 400),
                   (83, "pohon.webp", 900), (78, "daun-jatuh.webp", 1100)]:
    log.append((out, save_webp(trim_alpha(load(n)), out, mw, 84, alpha=True)))

# --- potongan foto struktur organisasi dari render halaman 4 ---------------
doc = pymupdf.open(PDF)
pg = doc[3]
ZOOM = 3.0                                   # 1170x828 -> 3510x2484
pix = pg.get_pixmap(matrix=pymupdf.Matrix(ZOOM * (1170 / pg.rect.width),
                                          ZOOM * (1170 / pg.rect.width)))
page4 = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
S = pix.width / 1170.0

boxes = {                                     # koordinat pada render 1170x828
    "komisaris":     (157, 150, 281, 300),
    "direktur-utama": (328, 252, 452, 400),
    "direktur":      (492, 253, 613, 405),
    "manager-adm":   (492, 480, 613, 625),
    "manager-ops":   (657, 480, 778, 625),
    "manager-mkt":   (829, 480, 950, 630),
}
for name, (x0, y0, x1, y1) in boxes.items():
    crop = page4.crop((round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S)))
    out = f"org/{name}.webp"
    log.append((out, save_webp(crop, out, 420, 86)))

# --- galeri ---------------------------------------------------------------
galeri = {
    "keh": [25, 26, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 40, 43, 44],
    "lin": [45, 47, 48, 49, 50, 51, 52, 54, 55, 56, 57, 58, 59, 60, 61],
    "man": [62, 63, 64, 65, 66, 67, 68, 69, 71, 72, 73, 74, 75, 76, 77],
}
for kode, nums in galeri.items():
    for i, n in enumerate(nums, 1):
        im = load(n)
        big = f"galeri/{kode}-{i:02d}.webp"
        th = f"galeri/th/{kode}-{i:02d}.webp"
        save_webp(im, big, 1100, 78)
        save_webp(im, th, 520, 72)
        log.append((big, os.path.getsize(os.path.join(DEST, big))))

total = 0
for name, info in log:
    if isinstance(info, tuple):
        print(f"{name:34s} {info[0]}x{info[1]}")
    else:
        total += info
        print(f"{name:34s} {info//1024} KB")
print(f"\ntotal webp: {total//1024} KB, berkas: {len(log)}")
