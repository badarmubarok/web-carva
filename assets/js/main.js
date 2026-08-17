/* PT Abhinaya Carva Utama — perilaku situs. Vanilla JS, tanpa dependency.
   Dipakai bersama oleh versi satu halaman dan versi multi-halaman. */
(function () {
  'use strict';

  var root = document.documentElement;
  var KEY = 'carva-lang';

  /* --- Dwibahasa -----------------------------------------------------------
     Kedua bahasa ditulis langsung di HTML (data-l="id" / data-l="en");
     CSS menyembunyikan yang tidak aktif. Default Inggris (permintaan pemilik
     situs); pilihan pengunjung disimpan di localStorage. */
  function setLang(lang) {
    lang = (lang === 'id') ? 'id' : 'en';
    root.setAttribute('data-lang', lang);
    root.setAttribute('lang', lang);
    try { localStorage.setItem(KEY, lang); } catch (e) {}
    document.querySelectorAll('.lang button').forEach(function (b) {
      b.setAttribute('aria-pressed', String(b.dataset.lang === lang));
    });
    document.querySelectorAll('[data-l-alt]').forEach(function (el) {
      var pair = el.dataset.lAlt.split('|');       /* "teks id|teks en" */
      var t = (lang === 'id' ? pair[0] : pair[1]) || pair[0];
      if (el.hasAttribute('placeholder')) el.setAttribute('placeholder', t);
      else if (el.hasAttribute('aria-label')) el.setAttribute('aria-label', t);
      else el.textContent = t;
    });
  }

  var saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  setLang(saved || 'en');

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.lang button');
    if (btn) setLang(btn.dataset.lang);
  });

  /* --- Navigasi ponsel ---------------------------------------------------- */
  var burger = document.querySelector('.burger');
  var links = document.querySelector('.nav-links');
  if (burger && links) {
    burger.addEventListener('click', function () {
      var open = links.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', String(open));
    });
    links.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        links.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* --- Header menempel ---------------------------------------------------- */
  var header = document.querySelector('.site-header');
  if (header) {
    var stick = function () { header.classList.toggle('is-stuck', window.scrollY > 8); };
    stick();
    window.addEventListener('scroll', stick, { passive: true });
  }

  /* --- Animasi muncul saat digulir ---------------------------------------- */
  var targets = document.querySelectorAll('.reveal');
  if (targets.length) {
    if (!('IntersectionObserver' in window) ||
        window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      targets.forEach(function (el) { el.classList.add('is-in'); });
    } else {
      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (!en.isIntersecting) return;
          en.target.style.transitionDelay = (en.target.dataset.delay || 0) + 'ms';
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: .06 });
      targets.forEach(function (el) { io.observe(el); });
      /* Jaring pengaman: tab dibuka di latar belakang atau halaman pendek. */
      window.setTimeout(function () {
        document.querySelectorAll('.reveal:not(.is-in)').forEach(function (el) {
          el.classList.add('is-in');
        });
      }, 2500);
    }
  }

  /* --- Penghitung angka --------------------------------------------------- */
  var counters = document.querySelectorAll('[data-count]');
  if (counters.length && 'IntersectionObserver' in window) {
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var co = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        var el = en.target, to = parseFloat(el.dataset.count), suf = el.dataset.suffix || '';
        co.unobserve(el);
        if (isNaN(to)) return;          /* jangan pernah menulis "NaN" ke halaman */
        if (reduce) { el.textContent = to + suf; return; }
        var t0 = null;
        (function step(ts) {
          if (t0 === null) t0 = ts;
          var p = Math.min((ts - t0) / 1300, 1);
          el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))) + suf;
          if (p < 1) requestAnimationFrame(step);
        })(performance.now());
      });
    }, { threshold: .4 });
    counters.forEach(function (el) { co.observe(el); });
  }

  /* --- Penyaring daftar (portofolio & tim ahli) ---------------------------
     Satu penangan untuk semua .filters: atribut data-target menunjuk wadah,
     data-item kelas kartu, dan data-key atribut yang dibandingkan. */
  function pick1(sel) { return sel ? document.querySelector(sel) : null; }

  document.querySelectorAll('.filters').forEach(function (bar) {
    var box = pick1(bar.dataset.target);
    if (!box) return;
    var itemSel = bar.dataset.item || '.pf-item';
    var key = bar.dataset.key || 'cat';

    function apply() {
      var pick = bar.querySelector('button[aria-pressed="true"]');
      pick = pick ? pick.dataset.filter : 'all';
      var input = pick1(bar.dataset.search);
      var q = input ? input.value.trim().toLowerCase() : '';
      var shown = 0;
      box.querySelectorAll(itemSel).forEach(function (card) {
        var okCat = pick === 'all' || card.dataset[key] === pick;
        var okQ = !q || card.textContent.toLowerCase().indexOf(q) > -1;
        card.classList.toggle('is-hidden', !(okCat && okQ));
        if (okCat && okQ) shown++;
      });
      var empty = box.querySelector('.pf-empty');
      if (empty) empty.classList.toggle('is-hidden', shown > 0);
      /* Jumlah yang tampil bisa muncul dua kali (teks ID dan EN) — perbarui
         semuanya. Atribut sengaja bernama data-tally, bukan data-count, agar
         tidak tertangkap animasi penghitung angka di atas. */
      if (bar.dataset.tally) {
        document.querySelectorAll(bar.dataset.tally).forEach(function (el) {
          el.textContent = shown;
        });
      }
    }

    bar.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      bar.querySelectorAll('button').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });
      apply();
    });

    var input = pick1(bar.dataset.search);
    if (input) input.addEventListener('input', apply);
    apply();
  });

  /* --- Tab galeri --------------------------------------------------------- */
  document.querySelectorAll('[data-tabs]').forEach(function (bar) {
    bar.addEventListener('click', function (e) {
      var btn = e.target.closest('button');
      if (!btn) return;
      bar.querySelectorAll('button').forEach(function (b) {
        b.setAttribute('aria-pressed', String(b === btn));
      });
      var pick = btn.dataset.tab;
      document.querySelectorAll('[data-panel]').forEach(function (p) {
        p.classList.toggle('is-hidden', p.dataset.panel !== pick);
      });
      /* Panel yang baru tampil tadi berlebar 0 — minta slider menghitung ulang. */
      window.dispatchEvent(new Event('resize'));
    });
  });

  /* --- Slider galeri ------------------------------------------------------
     Bergeser satu "layar penuh" per klik, bukan satu slide, supaya terasa
     wajar baik saat tampil 1 slide (ponsel) maupun 3 slide (desktop). Posisi
     dibaca dari scrollLeft sehingga tetap akurat walau pengguna menggeser
     sendiri lewat sentuhan atau trackpad. */
  document.querySelectorAll('[data-slider]').forEach(function (box) {
    var track = box.querySelector('.slider-track');
    if (!track) return;
    var prev = box.querySelector('.slider-prev');
    var next = box.querySelector('.slider-next');
    var cur = box.querySelector('.slider-cur');
    var bar = box.querySelector('.slider-progress i');
    var slides = track.querySelectorAll('.slide');
    var total = slides.length;

    function unit() {
      var w = slides[0] ? slides[0].getBoundingClientRect().width : 0;
      var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      return w + gap;
    }
    /* Satu klik = satu layar penuh. Dibulatkan (bukan dibulatkan ke bawah)
       karena lebar track pas berisi N slide + (N-1) jarak: pembulatan ke bawah
       akan menggeser N-1 slide saja dan menyisakan slide setengah terlihat. */
    function step() {
      var u = unit();
      if (!u) return track.clientWidth;
      return Math.max(1, Math.round(track.clientWidth / u)) * u;
    }
    function sync() {
      if (!track.clientWidth) return;              /* panel sedang disembunyikan */
      var max = track.scrollWidth - track.clientWidth;
      var x = track.scrollLeft;
      if (prev) prev.disabled = x <= 2;
      if (next) next.disabled = x >= max - 2;

      var u = unit() || track.clientWidth;
      var perView = Math.max(1, Math.round(track.clientWidth / u));
      var first = Math.min(Math.max(Math.round(x / u) + 1, 1), total);
      var last = Math.min(first + perView - 1, total);
      if (cur) cur.textContent = (first === last) ? first : first + '–' + last;
      if (bar) {
        var w = (perView / total) * 100;
        bar.style.width = w + '%';
        bar.style.left = (max > 0 ? (x / max) * (100 - w) : 0) + '%';
      }
    }
    /* Gulir halus berarti scrollLeft belum final saat handler selesai, dan
       event scroll bisa tertahan — status disegarkan beberapa kali. */
    function nudge(dir) {
      track.scrollLeft += dir * step();
      sync();
      [60, 200, 420].forEach(function (ms) { window.setTimeout(sync, ms); });
    }

    if (prev) prev.addEventListener('click', function () { nudge(-1); });
    if (next) next.addEventListener('click', function () { nudge(1); });
    track.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  });

  /* --- Lightbox galeri ---------------------------------------------------- */
  var lb = document.querySelector('.lightbox');
  if (lb) {
    var lbImg = lb.querySelector('img');
    var lbCap = lb.querySelector('.lb-cap');
    var shots = [], at = -1;

    /* Wadah panel galeri SEKALIGUS elemen .gal, jadi tombolnya anak langsung —
       cari 'button[data-full]', bukan '.gal button' (yang menuntut .gal di
       dalam panel dan tidak akan pernah cocok). */
    function collect(btn) {
      var panel = btn.closest('[data-panel]') || btn.closest('.gal') || document;
      shots = [].slice.call(panel.querySelectorAll('button[data-full]'));
      at = shots.indexOf(btn);
    }
    function show(i) {
      if (!shots.length) return;
      at = (i + shots.length) % shots.length;
      var b = shots[at], thumb = b.querySelector('img');
      lbImg.src = b.dataset.full || thumb.src;
      lbImg.alt = thumb.alt || '';
      lbCap.textContent = (at + 1) + ' / ' + shots.length + (thumb.alt ? ' — ' + thumb.alt : '');
    }
    function open(btn) { collect(btn); show(at); lb.classList.add('is-open'); document.body.style.overflow = 'hidden'; }
    function close() { lb.classList.remove('is-open'); lbImg.removeAttribute('src'); document.body.style.overflow = ''; }

    document.addEventListener('click', function (e) {
      var btn = e.target.closest('.slide[data-full]');
      if (btn) { open(btn); return; }
      if (e.target.closest('.lb-close') || e.target === lb) { close(); return; }
      if (e.target.closest('.lb-next')) { show(at + 1); return; }
      if (e.target.closest('.lb-prev')) { show(at - 1); }
    });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'ArrowRight') show(at + 1);
      if (e.key === 'ArrowLeft') show(at - 1);
    });
  }

  /* --- Formulir kontak ----------------------------------------------------
     Situs statis tanpa backend: pesan disusun lalu diserahkan ke aplikasi
     surel pengguna lewat mailto:. Tidak ada data yang dikirim ke pihak lain. */
  var form = document.getElementById('contact-form');
  if (form) {
    var TO = 'abhinayacarvautama@carva.co.id';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!form.reportValidity()) return;
      var v = function (id) { var el = form.querySelector('#' + id); return (el && el.value) || '-'; };
      var en = root.getAttribute('data-lang') === 'en';
      var subject = (en ? 'Website enquiry — ' : 'Permintaan dari website — ') + v('nama') +
                    (v('perusahaan') !== '-' ? ' (' + v('perusahaan') + ')' : '');
      var body = [
        (en ? 'Name' : 'Nama') + ': ' + v('nama'),
        (en ? 'Company / Institution' : 'Perusahaan / Instansi') + ': ' + v('perusahaan'),
        (en ? 'Email' : 'Surel') + ': ' + v('surel'),
        (en ? 'Phone' : 'Telepon') + ': ' + v('telepon'),
        (en ? 'Service of interest' : 'Layanan yang diminati') + ': ' + v('layanan'),
        '',
        (en ? 'Message' : 'Pesan') + ':',
        v('pesan')
      ].join('\n');
      window.location.href = 'mailto:' + TO +
        '?subject=' + encodeURIComponent(subject) +
        '&body=' + encodeURIComponent(body);
    });
  }

  /* --- Tahun berjalan di footer ------------------------------------------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
