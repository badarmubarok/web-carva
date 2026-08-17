# Membuat logo situs (assets/img/logo-carva.png) + favicon dari logo resmi
# CARVA yang dipakai situs lama: https://carva.co.id/images/CARVA21.jpg
# (salinannya: tools/logo-sumber-CARVA21.jpg).
#
# Versi ini dipilih pemilik situs karena warnanya solid dan garisnya lebih
# tajam daripada logo hasil ekstraksi company profile PDF (skrip build-aset*.py
# menulis versi PDF itu ke logo-carva-dari-pdf.png — JANGAN dipakai untuk situs).
#
# Latar putih JPEG diubah menjadi transparan lewat kanal TERKECIL: setiap warna
# logo (hijau, emas) selalu punya satu kanal jauh di bawah 255, sedangkan latar
# putih tidak. Sisa halo tipis masih ada di tepi (batas kualitas sumber JPEG) —
# karena itu logo di footer diletakkan di atas panel putih, bukan langsung di
# atas hijau tua.
import os
from PIL import Image

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo-sumber-CARVA21.jpg")
DEST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "img")
LO, HI = 208, 236          # <=LO opak penuh, >=HI transparan penuh

im = Image.open(SRC).convert("RGB")
w, h = im.size
px = im.load()
out = Image.new("RGBA", (w, h))
op = out.load()
for y in range(h):
    for x in range(w):
        r, g, b = px[x, y]
        m = min(r, g, b)
        a = 0 if m >= HI else (255 if m <= LO else int(255 * (HI - m) / (HI - LO)))
        op[x, y] = (r, g, b, a)

out = out.crop(out.getchannel("A").getbbox())
out.save(os.path.join(DEST, "logo-carva.png"), optimize=True)

side = max(out.size)
fav = Image.new("RGBA", (side, side), (0, 0, 0, 0))
fav.paste(out, ((side - out.width) // 2, (side - out.height) // 2))
fav.resize((180, 180), Image.LANCZOS).save(os.path.join(DEST, "favicon.png"), optimize=True)

print("logo-carva.png", out.size, "→ ingat: atribut width/height di 9 berkas HTML"
      " harus sama dengan ukuran ini")
