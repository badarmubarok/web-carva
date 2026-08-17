# Membuat berkas ZIP situs siap unggah manual ke cPanel (public_html).
#
# WAJIB dijalankan setiap kali ada revisi isi situs — pemilik situs mengunggah
# sendiri lewat cPanel, jadi ZIP yang basi berarti yang tayang bukan versi
# terbaru. Urutan kerja tiap revisi:
#     1. sunting index.html
#     2. python tools/gen-multi-halaman.py     (samakan versi multi-halaman)
#     3. python tools/buat-zip.py              (skrip ini)
#     4. git commit + push                     (GitHub Pages ikut terbarui)
#
# Dua varian dihasilkan:
#   …-LENGKAP.zip             semua berkas, termasuk company profile 52 MB
#   …-tanpa-pdf-besar.zip     tanpa PDF 52 MB (unggahan cepat / dibatasi ukuran)
#
# Pemakaian:  python tools/buat-zip.py [YYYY-MM-DD]
# Tanpa argumen memakai tanggal hari ini.
import os
import re
import sys
import zipfile
from datetime import date

SRC = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUT = r"D:\Desktop\@arsip\web carva"
PDF_BESAR = "assets/dok/Company-Profile-PT-Abhinaya-Carva-Utama-2026.pdf"

# Tidak ikut diunggah ke hosting: dokumentasi internal, skrip build, data git.
SKIP_DIR = {".git", "tools", "deploy", "__pycache__"}
SKIP_FILE = {"README.md", ".gitignore"}

stamp = sys.argv[1] if len(sys.argv) > 1 else date.today().isoformat()
if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", stamp):
    raise SystemExit("format tanggal harus YYYY-MM-DD")

items = []
for root, dirs, files in os.walk(SRC):
    dirs[:] = [d for d in dirs if d not in SKIP_DIR]
    for f in files:
        if f in SKIP_FILE:
            continue
        full = os.path.join(root, f)
        items.append((full, os.path.relpath(full, SRC).replace(os.sep, "/")))
items.sort(key=lambda x: x[1])

if not any(rel == "index.html" for _, rel in items):
    raise SystemExit("index.html tidak ditemukan — jalankan dari dalam proyek web_carva")

varian = [
    (f"carva-situs-{stamp}-LENGKAP.zip", items),
    (f"carva-situs-{stamp}-tanpa-pdf-besar.zip", [i for i in items if i[1] != PDF_BESAR]),
]

for nama, isi in varian:
    path = os.path.join(OUT, nama)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for full, rel in isi:
            z.write(full, rel)
    with zipfile.ZipFile(path) as z:
        rusak = z.testzip()
        html = z.read("index.html").decode("utf8")
    tahun = [int(t) for t in re.findall(r'<div class="pf-year">(\d{4})</div>', html)]
    urut = all(tahun[i] >= tahun[i + 1] for i in range(len(tahun) - 1))
    print(f"{nama:44s} {len(isi):>4} berkas  {os.path.getsize(path)/1048576:6.1f} MB  "
          f"integritas={'OK' if rusak is None else 'RUSAK'}  "
          f"portofolio={len(tahun)} butir, terbaru-di-atas={urut}")

print(f"\nTersimpan di: {OUT}")
print("Langkah unggah: CARA-UNGGAH-KE-CARVA.CO.ID.txt di folder yang sama.")
