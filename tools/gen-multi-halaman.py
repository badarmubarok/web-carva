# Membangkitkan versi MULTI-HALAMAN dari index.html (versi satu halaman)
# supaya isi kedua versi tidak pernah berbeda. Jalankan ulang setiap kali
# index.html berubah.
import io, os, re

ROOT = r"D:\Kerjaan\ayah\@proyek_saya\web_carva"
src = io.open(os.path.join(ROOT, "index.html"), encoding="utf8").read()

# --- ambil bagian-bagian dari index.html -----------------------------------
def section(sid):
    m = re.search(r'<section class="[^"]*" id="' + sid + r'">.*?\n</section>', src, re.S)
    if not m:
        raise SystemExit("section tidak ditemukan: " + sid)
    return m.group(0)

def hero():
    m = re.search(r'<section class="hero" id="beranda">.*?\n</section>', src, re.S)
    return m.group(0)

SEC = {s: section(s) for s in
       ("tentang", "visi-misi", "cara-kerja", "layanan", "portofolio", "tim", "galeri", "klien", "kontak")}

# --- penyesuaian untuk halaman terpisah ------------------------------------
PAGE_OF = {
    "#beranda": "multi-halaman.html", "#tentang": "tentang.html", "#visi-misi": "tentang.html#visi-misi",
    "#cara-kerja": "tentang.html#cara-kerja", "#layanan": "layanan.html", "#portofolio": "portofolio.html",
    "#tim": "tim-ahli.html", "#galeri": "galeri.html", "#klien": "klien.html", "#kontak": "kontak.html",
}

def relink(html):
    def sub(m):
        return 'href="' + PAGE_OF.get(m.group(1), m.group(1)) + '"'
    return re.sub(r'href="(#[a-z-]+)"', sub, html)

def as_h1(html):
    """Judul utama halaman: naikkan <h2> pertama di .sec-head menjadi <h1>."""
    return re.sub(r'<h2>(.*?)</h2>', r'<h1 class="page-h1">\1</h1>', html, count=1, flags=re.S)

def first_section(html):
    html = re.sub(r'<section class="sec([^"]*)"', r'<section class="sec sec-top\1"', html, count=1)
    return as_h1(html)

# --- kerangka halaman ------------------------------------------------------
NAV = [
    ("multi-halaman.html", "Home", "Beranda"),
    ("tentang.html", "About", "Tentang"),
    ("layanan.html", "Services", "Layanan"),
    ("portofolio.html", "Portfolio", "Portofolio"),
    ("tim-ahli.html", "Team", "Tim"),
    ("galeri.html", "Gallery", "Galeri"),
    ("klien.html", "Clients", "Klien"),
    ("kontak.html", "Contact", "Kontak"),
]

def nav(active):
    out = []
    for href, en, idn in NAV:
        cur = ' aria-current="page"' if href == active else ''
        out.append(f'      <a href="{href}"{cur}><span data-l="en">{en}</span><span data-l="id">{idn}</span></a>')
    return "\n".join(out)

FOOT_EXPLORE = "\n".join(
    f'          <li><a href="{href}"><span data-l="en">{en}</span><span data-l="id">{idn}</span></a></li>'
    for href, en, idn in NAV[1:])

def shell(fname, title, desc, active, body, og_img="assets/img/hero-hutan.webp"):
    return f'''<!DOCTYPE html>
<html lang="en" data-lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="author" content="PT Abhinaya Carva Utama">
<link rel="canonical" href="https://carva.co.id/{fname}">
<meta name="theme-color" content="#1b5e20">
<meta property="og:type" content="website">
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="id_ID">
<meta property="og:site_name" content="PT Abhinaya Carva Utama">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="https://carva.co.id/{fname}">
<meta property="og:image" content="https://carva.co.id/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="assets/img/favicon.png">
<link rel="apple-touch-icon" href="assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="assets/css/style.css">
<link rel="stylesheet" href="assets/css/onepage.css">
</head>
<body>
<a class="skip" href="#isi"><span data-l="en">Skip to content</span><span data-l="id">Lompat ke konten</span></a>
<div class="progress" aria-hidden="true"><i></i></div>

<header class="site-header">
  <div class="wrap header-in">
    <a class="brand" href="multi-halaman.html" aria-label="PT Abhinaya Carva Utama">
      <img src="assets/img/logo-carva.png" alt="Logo CARVA — PT Abhinaya Carva Utama" width="617" height="409">
      <b>Abhinaya<br>Carva<br>Utama</b>
    </a>

    <button class="burger" aria-label="Menu" aria-expanded="false" aria-controls="menu"><span></span></button>

    <div class="lang" role="group" aria-label="Language / Bahasa">
      <button type="button" data-lang="en" aria-pressed="true">EN</button>
      <button type="button" data-lang="id" aria-pressed="false">ID</button>
    </div>

    <a class="btn btn-sm nav-cta" href="kontak.html"><span data-l="en">Get in touch</span><span data-l="id">Hubungi kami</span></a>

    <nav class="nav-links" id="menu" aria-label="Main">
{nav(active)}
    </nav>
  </div>
</header>

<main id="isi">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <img class="flogo" src="assets/img/logo-carva.png" alt="CARVA" width="617" height="409" loading="lazy">
        <p><b>PT Abhinaya Carva Utama</b><br>
          <span data-l="en">Management &amp; environmental consultant for forestry, plantation, agriculture and mining.</span>
          <span data-l="id">Konsultan manajemen &amp; lingkungan untuk kehutanan, perkebunan, pertanian, dan pertambangan.</span>
        </p>
        <p class="foot-motto">“beyond your expectations”</p>
      </div>
      <div>
        <h4 data-l-alt="Jelajahi|Explore">Explore</h4>
        <ul>
{FOOT_EXPLORE}
          <li><a href="index.html"><span data-l="en">One-page version</span><span data-l="id">Versi satu halaman</span></a></li>
        </ul>
      </div>
      <div>
        <h4 data-l-alt="Layanan|Services">Services</h4>
        <ul>
          <li><span data-l="en">Forestry</span><span data-l="id">Kehutanan</span></li>
          <li><span data-l="en">Environment</span><span data-l="id">Lingkungan</span></li>
          <li><span data-l="en">Management &amp; training</span><span data-l="id">Manajemen &amp; pelatihan</span></li>
          <li>ISO 9001:2015</li>
          <li>ISO 45001:2018</li>
        </ul>
      </div>
      <div>
        <h4 data-l-alt="Kontak|Contact">Contact</h4>
        <ul>
          <li>Villa Ciomas Indah, Jl. Maleo III Blok G15 No. 18, Ciomas, Kab. Bogor</li>
          <li><a href="tel:+6281802920809">+62 818-0292-0809</a></li>
          <li><a href="mailto:abhinayacarvautama@carva.co.id">abhinayacarvautama@carva.co.id</a></li>
          <li><a href="assets/dok/Company-Profile-PT-Abhinaya-Carva-Utama-2026-ringan.pdf" download><span data-l="en">Company Profile 2026 (3.6 MB)</span><span data-l="id">Company Profile 2026 (3,6 MB)</span></a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bot">
      <span>© <span data-year>2026</span> PT Abhinaya Carva Utama. <span data-l="en">All rights reserved.</span><span data-l="id">Seluruh hak dilindungi.</span></span>
      <span class="alt-view"><a href="https://elps.co.id" target="_blank" rel="noopener"><span data-l="id">Website dalam pengelolaan PT. Eka Lestari Persada (ELPS)</span><span data-l="en">Website managed by PT Eka Lestari Persada (ELPS)</span></a></span>
    </div>
  </div>
</footer>

<button class="totop" aria-label="Back to top" data-l-alt="Kembali ke atas|Back to top">
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20V6"/><path d="m6 11 6-6 6 6"/></svg>
</button>

<div class="lightbox" role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="lb-close" type="button" aria-label="Close">×</button>
  <button class="lb-prev" type="button" aria-label="Previous">‹</button>
  <button class="lb-next" type="button" aria-label="Next">›</button>
  <div>
    <img alt="">
    <p class="lb-cap"></p>
  </div>
</div>

<script src="assets/js/main.js"></script>
<script src="assets/js/onepage.js"></script>
</body>
</html>
'''

# --- ajakan penutup (dipakai di beberapa halaman) --------------------------
CTA = '''<section class="sec">
  <div class="wrap">
    <div class="cta reveal">
      <div>
        <h2><span data-l="en">Need the full company profile?</span><span data-l="id">Perlu company profile lengkap?</span></h2>
        <p><span data-l="en">The 2026 edition covers our legal data, certification, organisation, expert team, all 46 assignments and field documentation.</span><span data-l="id">Edisi 2026 memuat data legal, sertifikasi, struktur organisasi, tim ahli, seluruh 46 penugasan, dan dokumentasi lapangan.</span></p>
      </div>
      <div class="cta-actions">
        <a class="btn btn-gold" href="assets/dok/Company-Profile-PT-Abhinaya-Carva-Utama-2026-ringan.pdf" download><span data-l="en">Download (3.6 MB)</span><span data-l="id">Unduh (3,6 MB)</span></a>
        <a class="btn btn-light" href="kontak.html"><span data-l="en">Contact us</span><span data-l="id">Hubungi kami</span></a>
      </div>
    </div>
  </div>
</section>'''

# --- beranda multi-halaman -------------------------------------------------
TEASER = '''<section class="sec sec-cream">
  <div class="wrap">
    <div class="about-grid">
      <div>
        <div class="sec-head">
          <span class="eyebrow"><span data-l="en">About us</span><span data-l="id">Tentang kami</span></span>
          <h2><span data-l="en">A consultant that stands beside its clients</span><span data-l="id">Konsultan yang berdiri di samping kliennya</span></h2>
        </div>
        <p><span data-l="en">PT Abhinaya Carva Utama is a management and environmental consultant focused on the forestry, plantation, agriculture and mining sectors — taking an active part in development that keeps economic, social and environmental aspects in balance.</span><span data-l="id">PT Abhinaya Carva Utama adalah konsultan manajemen dan lingkungan untuk sektor kehutanan, perkebunan, pertanian, dan pertambangan — berpartisipasi aktif dalam pembangunan yang seimbang antara aspek ekonomi, sosial, dan lingkungan.</span></p>
        <blockquote class="quote">
          <p><span data-l="en">We call the relationship with our clients <b>“reciprocity and mutual trust”</b> — an exchange of value that runs both ways, kept together by trust that is earned on every assignment.</span><span data-l="id">Hubungan dengan pelanggan/klien kami sebut sebagai <b>“reciprocity and mutual trust”</b> — pertukaran nilai yang berjalan dua arah, dijaga oleh kepercayaan yang dibangun pada setiap penugasan.</span></p>
        </blockquote>
        <p style="margin-top:1.4rem"><a class="btn btn-ghost" href="tentang.html"><span data-l="en">More about us</span><span data-l="id">Selengkapnya tentang kami</span></a></p>
      </div>
      <div>
        <figure class="figure">
          <img src="assets/img/tim-lapangan.webp" alt="CARVA field team and client personnel at a forest concession" width="1229" height="692" loading="lazy">
          <figcaption><span data-l="en">Joint field team on a forest inventory assignment</span><span data-l="id">Tim lapangan gabungan pada pekerjaan inventarisasi hutan</span></figcaption>
        </figure>
        <div class="iso">
          <figure>
            <img src="assets/img/iso-9001.webp" alt="ISO 9001:2015 certificate" width="700" height="989" loading="lazy">
            <figcaption>ISO 9001:2015<small><span data-l="en">Quality Management System</span><span data-l="id">Sistem Manajemen Mutu</span></small></figcaption>
          </figure>
          <figure>
            <img src="assets/img/iso-45001.webp" alt="ISO 45001:2018 certificate" width="700" height="989" loading="lazy">
            <figcaption>ISO 45001:2018<small><span data-l="en">Occupational Health &amp; Safety</span><span data-l="id">Kesehatan &amp; Keselamatan Kerja</span></small></figcaption>
          </figure>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec-head center">
      <span class="eyebrow"><span data-l="en">What we do</span><span data-l="id">Yang kami kerjakan</span></span>
      <h2><span data-l="en">Three fields of service</span><span data-l="id">Tiga bidang layanan</span></h2>
    </div>
    <div class="grid g-3">
      <article class="card svc reveal">
        <div class="svc-img"><img src="assets/img/jasa-kehutanan.webp" alt="Production forest stand" width="1000" height="588" loading="lazy"></div>
        <div class="svc-body">
          <h3><span data-l="en">Forestry</span><span data-l="id">Kehutanan</span></h3>
          <p><span data-l="en">Carbon stock, IHMB, forestry permits (PPKH, PBPH, PAK), GIS mapping, rehabilitation, boundary demarcation, HCV.</span><span data-l="id">Sediaan karbon, IHMB, perizinan kehutanan (PPKH, PBPH, PAK), pemetaan GIS, rehabilitasi, tata batas, HCV.</span></p>
        </div>
      </article>
      <article class="card svc reveal" data-delay="90">
        <div class="svc-img"><img src="assets/img/jasa-lingkungan.webp" alt="Seedling growing in soil" width="1000" height="588" loading="lazy"></div>
        <div class="svc-body">
          <h3><span data-l="en">Environment</span><span data-l="id">Lingkungan</span></h3>
          <p><span data-l="en">AMDAL, UKL-UPL, DELH, DPLH, environmental monitoring (Monev), biodiversity survey, B3 waste permits.</span><span data-l="id">AMDAL, UKL-UPL, DELH, DPLH, monitoring dan evaluasi lingkungan, survey kehati, perizinan limbah B3.</span></p>
        </div>
      </article>
      <article class="card svc reveal" data-delay="180">
        <div class="svc-img"><img src="assets/img/jasa-manajemen.webp" alt="Desk with documents, tablet and calculator" width="1000" height="588" loading="lazy"></div>
        <div class="svc-body">
          <h3><span data-l="en">Management &amp; Training</span><span data-l="id">Manajemen &amp; Pelatihan</span></h3>
          <p><span data-l="en">Socioeconomic and satisfaction surveys, asset administration, HBU, business plan, SOP, policy studies, training.</span><span data-l="id">Survey sosial ekonomi dan kepuasan, penatausahaan aset, HBU, business plan, SOP, kajian kebijakan, pelatihan.</span></p>
        </div>
      </article>
    </div>
    <p style="text-align:center;margin-top:1.8rem"><a class="btn" href="layanan.html"><span data-l="en">See all services in detail</span><span data-l="id">Lihat rincian seluruh layanan</span></a></p>
  </div>
</section>'''

pages = {
    "multi-halaman.html": dict(
        title="PT Abhinaya Carva Utama — Management &amp; Environmental Consultant",
        desc="Indonesian management and environmental consultant for forestry, plantation, agriculture and mining: EIA (AMDAL), permits, carbon stock, HCV/HCS, GIS mapping and management training.",
        body=relink(hero()) + "\n\n" + TEASER + "\n\n" + CTA),
    "tentang.html": dict(
        title="About us — PT Abhinaya Carva Utama",
        desc="Company profile, legal data, ISO 9001:2015 and ISO 45001:2018 certification, vision, mission, working values and the four pillars behind every CARVA assignment.",
        body=first_section(relink(SEC["tentang"])) + "\n\n" + relink(SEC["visi-misi"]) + "\n\n" + relink(SEC["cara-kerja"]) + "\n\n" + CTA),
    "layanan.html": dict(
        title="Services — PT Abhinaya Carva Utama",
        desc="Forestry, environment, and management &amp; training services: carbon stock, IHMB, PPKH/PBPH permits, AMDAL, UKL-UPL, Monev, HCV/HCS, GIS mapping, SOP, feasibility studies and training.",
        body=first_section(relink(SEC["layanan"])) + "\n\n" + CTA),
    "portofolio.html": dict(
        title="Portfolio — PT Abhinaya Carva Utama",
        desc="46 assignments from 2022 to 2026 for private companies, state-owned enterprises, ministries, research institutions and international partners across Indonesia.",
        body=first_section(relink(SEC["portofolio"])) + "\n\n" + CTA),
    "tim-ahli.html": dict(
        title="Organisation &amp; expert team — PT Abhinaya Carva Utama",
        desc="Management structure and 25 experts across 15 fields: forest carbon, microbiology, biodiversity, silviculture, GIS and drone mapping, social, economics and finance.",
        body=first_section(relink(SEC["tim"])) + "\n\n" + CTA),
    "galeri.html": dict(
        title="Activity documentation — PT Abhinaya Carva Utama",
        desc="Forty-five photographs from CARVA's own assignments: forest inventory plots, peatland restoration, environmental surveys, workshops and training.",
        body=first_section(relink(SEC["galeri"])) + "\n\n" + CTA),
    "klien.html": dict(
        title="Clients — PT Abhinaya Carva Utama",
        desc="Ministries, state-owned enterprises, research institutions, international partners and private companies that have worked with PT Abhinaya Carva Utama.",
        body=first_section(relink(SEC["klien"])) + "\n\n" + CTA),
    "kontak.html": dict(
        title="Contact — PT Abhinaya Carva Utama",
        desc="Office address in Ciomas, Kabupaten Bogor, phone, WhatsApp, email and office hours of PT Abhinaya Carva Utama, plus a short enquiry form.",
        body=first_section(relink(SEC["kontak"]))),
}

for fname, cfg in pages.items():
    active = fname
    html = shell(fname, cfg["title"], cfg["desc"], active, cfg["body"])
    io.open(os.path.join(ROOT, fname), "w", encoding="utf8", newline="\n").write(html)
    print(f"{fname:22s} {len(html)//1024} KB")
