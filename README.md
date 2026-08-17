# Situs PT Abhinaya Carva Utama — carva.co.id

Situs profil perusahaan statis (HTML/CSS/JS, tanpa build step, tanpa dependency
runtime). Dibangun **17 Agustus 2026** dari dua sumber:

1. `D:\Desktop\@arsip\web carva\2026. COMPRO CARVA - 15082026.pdf`
   (company profile 2026, 16 halaman) — sumber utama seluruh isi.
2. Situs lama `https://carva.co.id/` — dipakai sebagai pembanding.

Situs ini **menggantikan** situs lama pada alamat yang sama.

## Dua versi berdampingan

| Berkas | Versi | Keterangan |
|---|---|---|
| `index.html` | **satu halaman** | Halaman utama. Semua isi dalam satu gulir + navigasi anchor, scrollspy, bilah kemajuan, tombol kembali ke atas. |
| `multi-halaman.html` + 7 berkas | multi-halaman | Beranda ringkas + `tentang` · `layanan` · `portofolio` · `tim-ahli` · `galeri` · `klien` · `kontak`. |

Keduanya saling tertaut lewat footer (kolom *Explore*). Keduanya memakai
`assets/css/style.css` + `assets/js/main.js` + `assets/css/onepage.css` +
`assets/js/onepage.js` yang sama — jadi tampilan dan perilakunya identik.
(`onepage.*` bukan hanya untuk versi satu halaman: di semua halaman ia
menyediakan bilah kemajuan gulir dan tombol kembali ke atas.)

**Menukar versi utama**: tukar nama `index.html` ⇄ `multi-halaman.html`, lalu
sesuaikan `canonical` di `<head>` keduanya dan `sitemap.xml`.

## Isi & keputusan

- **Dwibahasa ID + EN**, default **Inggris**. Kedua bahasa ditulis langsung di
  HTML (`<span data-l="id">` / `<span data-l="en">`); CSS menyembunyikan yang
  tidak aktif; pilihan pengunjung disimpan di `localStorage` (`carva-lang`).
  Untuk atribut (placeholder / aria-label / label pendek) dipakai
  `data-l-alt="teks id|teks en"` yang diisi oleh `main.js`.
- **46 penugasan** 2022–2026, bisa disaring per kategori dan dicari bebas.
  Sumber PDF mencantumkan PT Berkat Cahaya Timber dua kali (Jasa Konsultasi dan
  Lainnya) — di situs ditampilkan **satu kali**.
- **25 tenaga ahli** pada 15 bidang, disaring ke 6 kelompok bidang.
- **6 foto struktur organisasi** dipotong dari halaman 4 PDF (aslinya tidak
  tersimpan sebagai gambar utuh yang bisa diekstrak).
- **45 foto dokumentasi** dalam 3 slider (Kehutanan / Lingkungan / Manajemen &
  Pelatihan) + lightbox dengan navigasi papan tuas.
- **Data legal ditampilkan**: akta No. 131 (30/11/2021), notaris, SK
  Kemenkumham, NIB, dua sertifikat ISO. **NPWP sengaja TIDAK ditampilkan**
  (keputusan pemilik situs).
- **Data kontak** memakai versi PDF 2026 (Jl. Maleo III Blok G15 No. 18,
  +62 818-0292-0809, abhinayacarvautama@carva.co.id) — berbeda dari situs lama
  yang menulis Blok G1 No. 22 dan +62 813-8967-8598.
- **Ejaan sumber yang diperbaiki di situs**: “Sumatera Aelatan” → Sumatera
  Selatan · “KEMENTERAIN” → Kementerian · “Peatlend” → peatland ·
  “Bussiness” → Business · “Ekosisten” → ekosistem · “Graha Equilty” → Graha
  Equity (mengikuti tulisan resmi pada butir lain).
- **Formulir kontak** tanpa backend: menyusun pesan lalu menyerahkannya ke
  aplikasi surel pengunjung lewat `mailto:`. Tidak ada data yang dikirim ke
  pihak ketiga.
- **Peta** memakai sematan OpenStreetMap (tanpa kunci API, tanpa pelacak).
- Kredit footer kanan bawah: “Website dalam pengelolaan PT. Eka Lestari Persada
  (ELPS)” → https://elps.co.id, ukuran huruf sengaja lebih kecil dari baris hak
  cipta.

## Unduhan company profile

| Berkas | Ukuran | Catatan |
|---|---|---|
| `assets/dok/Company-Profile-…-2026-ringan.pdf` | 3,6 MB | **Tombol utama.** Tiap halaman dirender 150 dpi lalu dipasang sebagai JPEG q72 — tampilan identik dengan aslinya, teks tidak bisa diseleksi. |
| `assets/dok/Company-Profile-…-2026.pdf` | 52 MB | Asli, resolusi penuh (untuk tender/cetak). |

Kompresi bawaan pymupdf (`rewrite_images`) sempat dicoba: hasil 15,6 MB **tapi
latar langit/awan hilang** (`cannot find Pattern resource`), jadi tidak dipakai.

## Aset

Semua foto berasal dari company profile, dikonversi ke WebP (total ± 7,5 MB).
**Gotcha**: transparansi di PDF ini tersimpan pada *soft mask* terpisah —
mengekstrak gambar dasar saja menghasilkan latar hitam. Lihat
`tools/build-aset-transparan.py`.

**Logo situs bukan dari PDF.** Dipakai logo resmi yang juga dipakai situs lama
(`https://carva.co.id/images/CARVA21.jpg`, salinan di
`tools/logo-sumber-CARVA21.jpg`) karena warnanya solid dan garisnya lebih tajam;
latar putihnya dibuat transparan oleh `tools/build-logo.py` → `logo-carva.png`
(617×409) + `favicon.png`. Versi hasil ekstraksi PDF ditulis skrip aset ke
`logo-carva-dari-pdf.png` dan **tidak dipakai**.

Ukuran 617×409 tertulis pada atribut `width`/`height` di 9 berkas HTML — kalau
logo diganti lagi, ubah juga angka itu (dan di `tools/gen-multi-halaman.py`),
supaya tidak terjadi pergeseran tata letak saat gambar dimuat.

Logo footer diletakkan di atas panel putih: sumber JPEG menyisakan halo tipis di
tepi sehingga kurang bagus bila ditempel langsung di atas hijau tua. Versi
knockout putih lama (`logo-carva-putih.png`) masih tersimpan tetapi tidak
dipakai — ditolak karena guratan skrip logonya sendiri berwarna putih.

## Alat bantu (`tools/`)

Butuh Python + `pymupdf` + `Pillow` (mis. `E:\laragon\bin\python\312-64\python.exe`).

| Skrip | Fungsi |
|---|---|
| `build-aset.py` | Ekstrak & konversi gambar dari PDF ke `assets/img/` (termasuk galeri + thumbnail). |
| `build-aset-transparan.py` | Perbaiki dekorasi bertransparansi + potong 6 foto struktur organisasi. |
| `build-logo.py` | Logo situs + favicon dari `logo-sumber-CARVA21.jpg` (latar putih → transparan). |
| `gen-multi-halaman.py` | **Bangkitkan ulang seluruh versi multi-halaman dari `index.html`.** |

> Setiap kali `index.html` diubah, jalankan `gen-multi-halaman.py` agar versi
> multi-halaman tidak basi. Jangan mengedit 8 berkas multi-halaman secara
> manual — perubahannya akan tertimpa.

## Pratinjau lokal

Entri `web-carva` (port 5176) sudah ada di `.claude/launch.json` repo `simrhl`.
Atau:

```bash
npx --yes http-server "D:/Kerjaan/ayah/@proyek_saya/web_carva" -p 5176 -c-1
```

## Status deploy (17 Agustus 2026)

- **GitHub**: https://github.com/badarmubarok/web-carva (publik, cabang `main`).
- **Pratinjau tayang**: https://badarmubarok.github.io/web-carva/ — GitHub Pages
  dari `main` / root, 9 halaman + aset + PDF diverifikasi 200.
- **carva.co.id**: BELUM. Kredensial FTP/cPanel pada `kredensial carva.txt`
  ditolak server (`530 Login authentication failed`) di `103.7.226.28` maupun
  `103.7.226.172`, semua varian username; SSH tertutup. Situs diunggah manual
  lewat cPanel memakai berkas ZIP di `D:\Desktop\@arsip\web carva\`
  (`carva-situs-…-LENGKAP.zip` / `…-tanpa-pdf-besar.zip`), langkahnya di
  `CARA-UNGGAH-KE-CARVA.CO.ID.txt`.
- **Arsip situs lama**: `D:\Desktop\@arsip\web carva\backup-situs-lama-carva.co.id-2026-08-17\`
  — 45 berkas / 76 MB hasil mirror HTTP. 12 gambar galeri (folder `MHP` dan
  `SERTIF`) tidak terselamatkan karena **server aslinya membalas HTTP 500** untuk
  berkas-berkas itu; artinya gambar tersebut sudah rusak di situs lama.

## Deploy ke carva.co.id

Situs lama berada di hosting pihak ketiga: **103.7.226.28, server LiteSpeed**
(bukan VM sendiri). Karena itu unggahan dilakukan oleh pemilik akun hosting:

1. Masuk cPanel/File Manager (atau FTP) domain `carva.co.id`.
2. **Backup dulu** isi `public_html` yang sekarang (situs lama akan tergantikan).
3. Unggah seluruh isi folder ini ke `public_html` — kecuali `README.md` dan
   `tools/`. Struktur folder `assets/` harus ikut apa adanya.
4. Pastikan `index.html` berada di akar `public_html`.
5. Uji: halaman utama, unduh company profile, slider galeri, kirim formulir,
   dan sakelar ID/EN.

Berkas 52 MB (`…-2026.pdf`) boleh dilewati kalau kuota/hosting terbatas —
tombol “Full resolution” di halaman kontak perlu dihapus bila begitu.

Kalau nanti situs dipindah ke server sendiri, ubah `canonical` di 9 berkas HTML,
`sitemap.xml`, dan `robots.txt`.

## Yang belum ada (perlu dari klien)

- Logo klien (situs lama pun tidak punya) — bagian Klien memakai daftar nama.
- Koordinat pasti kantor: peta memakai titik perkiraan Ciomas
  (−6,5895 / 106,7585). Kirim titik Google Maps yang benar bila perlu tepat.
- Konfirmasi nomor telepon 2026 masih aktif (situs lama memakai nomor lain).
