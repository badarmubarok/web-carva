# Perbaikan: (1) gambar bertransparansi harus digabung dengan SMask-nya,
# (2) potongan foto struktur organisasi dipersempit agar label & titik
#     konektor tidak ikut terpotong.
import io, os
import pymupdf
from PIL import Image

PDF = r"D:\Desktop\@arsip\web carva\2026. COMPRO CARVA - 15082026.pdf"
DEST = r"D:\Kerjaan\ayah\@proyek_saya\web_carva\assets\img"
doc = pymupdf.open(PDF)

# xref -> smask xref
smask = {}
for page in doc:
    for info in page.get_images(full=True):
        smask[info[0]] = info[1]


def rgba(xref):
    base = pymupdf.Pixmap(doc, xref)
    m = smask.get(xref, 0)
    if m:
        pix = pymupdf.Pixmap(base, pymupdf.Pixmap(doc, m))
    else:
        pix = base
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")
    bb = im.getchannel("A").getbbox()
    return im.crop(bb) if bb else im


def scale(im, maxw):
    return im if im.width <= maxw else im.resize(
        (maxw, round(im.height * maxw / im.width)), Image.LANCZOS)


# --- logo -----------------------------------------------------------------
logo = rgba(1121)
logo.save(os.path.join(DEST, "logo-carva-dari-pdf.png"), optimize=True)
print("logo-carva-dari-pdf.png", logo.size)

putih = logo.copy()
px = putih.load()
for y in range(putih.height):
    for x in range(putih.width):
        r, g, b, a = px[x, y]
        if a:
            px[x, y] = (255, 255, 255, a)
putih.save(os.path.join(DEST, "logo-carva-putih.png"), optimize=True)

side = max(logo.size)
fav = Image.new("RGBA", (side, side), (0, 0, 0, 0))
fav.paste(logo, ((side - logo.width) // 2, (side - logo.height) // 2))
fav.resize((180, 180), Image.LANCZOS).save(os.path.join(DEST, "favicon-dari-pdf.png"), optimize=True)

# --- dekorasi bertransparansi --------------------------------------------
for xref, out, mw in [(1681, "globe-lumut.webp", 900), (775, "daun.webp", 400),
                      (1129, "pohon.webp", 900), (1106, "daun-jatuh.webp", 1100)]:
    im = scale(rgba(xref), mw)
    im.save(os.path.join(DEST, out), "WEBP", quality=84, method=6, lossless=False)
    print(out, im.size, os.path.getsize(os.path.join(DEST, out)) // 1024, "KB")

# --- potongan struktur organisasi ---------------------------------------
pg = doc[3]
z = 3.0 * (1170 / pg.rect.width)
pix = pg.get_pixmap(matrix=pymupdf.Matrix(z, z))
page4 = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
S = pix.width / 1170.0
boxes = {
    "komisaris":      (159, 152, 279, 288),
    "direktur-utama": (330, 254, 450, 396),
    "direktur":       (494, 256, 611, 400),
    "manager-adm":    (495, 496, 610, 622),
    "manager-ops":    (660, 496, 775, 622),
    "manager-mkt":    (832, 496, 947, 628),
}
for name, (x0, y0, x1, y1) in boxes.items():
    crop = page4.crop((round(x0 * S), round(y0 * S), round(x1 * S), round(y1 * S)))
    crop = scale(crop.convert("RGB"), 420)
    crop.save(os.path.join(DEST, f"org/{name}.webp"), "WEBP", quality=86, method=6)
print("org crops ok")
