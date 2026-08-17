/* Tambahan khusus versi SATU HALAMAN. Dimuat setelah main.js, yang sudah
   menangani dwibahasa, navigasi, animasi, penghitung, penyaring, tab galeri,
   lightbox, dan formulir kontak. */
(function () {
  'use strict';

  var HEADER = 76; /* --header-h pada style.css */

  /* --- Penanda section aktif saat digulir (scrollspy) --------------------- */
  var links = [].slice.call(document.querySelectorAll('.nav-links a[href^="#"]'));
  var map = {}, sections = [];
  links.forEach(function (a) {
    var el = document.getElementById(a.getAttribute('href').slice(1));
    if (!el) return;
    map[el.id] = a;
    sections.push(el);
  });

  if (sections.length && 'IntersectionObserver' in window) {
    var visible = {};
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { visible[en.target.id] = en.isIntersecting; });
      var current = null;
      sections.forEach(function (s) { if (visible[s.id] && !current) current = s.id; });
      links.forEach(function (a) { a.removeAttribute('aria-current'); });
      if (current && map[current]) map[current].setAttribute('aria-current', 'true');
    }, { rootMargin: '-' + HEADER + 'px 0px -55% 0px', threshold: 0 });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* --- Bilah kemajuan gulir ---------------------------------------------- */
  var bar = document.querySelector('.progress i');
  if (bar) {
    var draw = function () {
      var h = document.documentElement.scrollHeight - window.innerHeight;
      bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + '%';
    };
    draw();
    window.addEventListener('scroll', draw, { passive: true });
    window.addEventListener('resize', draw);
  }

  /* --- Tombol kembali ke atas -------------------------------------------- */
  var btn = document.querySelector('.totop');
  if (btn) {
    var toggle = function () { btn.classList.toggle('is-on', window.scrollY > 700); };
    toggle();
    window.addEventListener('scroll', toggle, { passive: true });
    btn.addEventListener('click', function () {
      var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
  }
})();
