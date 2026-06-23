// A to Z Enterprises — main.js

document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  const navToggle = document.getElementById('navToggle');
  const mainNav = document.getElementById('mainNav');

  if (navToggle && mainNav) {
    navToggle.addEventListener('click', function () {
      const isOpen = mainNav.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    // Close menu when a link is tapped
    mainNav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        mainNav.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // Auto-dismiss flash messages after 6 seconds
  document.querySelectorAll('.flash').forEach(function (flash) {
    setTimeout(function () {
      flash.style.opacity = '0';
      flash.style.transition = 'opacity 0.4s ease';
      setTimeout(function () { flash.remove(); }, 400);
    }, 6000);
  });

  // Product category filter chips (client-side highlight, server handles actual filtering via link)
  document.querySelectorAll('.chip[data-category]').forEach(function (chip) {
    chip.addEventListener('click', function (e) {
      // Links navigate normally; this just gives instant visual feedback
      document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
    });
  });
});
