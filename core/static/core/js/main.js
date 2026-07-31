(function () {
    'use strict';

    // ---- AOS (scroll animations) ----
    if (window.AOS) {
        AOS.init({
            duration: 700,
            once: true,
            offset: 60,
        });
    }

    // ---- Footer year ----
    const yearEl = document.getElementById('currentYear');
    if (yearEl) {
        yearEl.textContent = new Date().getFullYear();
    }

    // ---- Dark / Light mode toggle ----
    const root = document.documentElement;
    const toggleBtn = document.getElementById('themeToggle');
    const iconDark = document.getElementById('themeIconDark'); // shown in light mode (click to go dark)
    const iconLight = document.getElementById('themeIconLight'); // shown in dark mode (click to go light)

    function applyTheme(theme) {
        root.setAttribute('data-bs-theme', theme);
        if (theme === 'dark') {
            iconDark && iconDark.classList.add('d-none');
            iconLight && iconLight.classList.remove('d-none');
        } else {
            iconDark && iconDark.classList.remove('d-none');
            iconLight && iconLight.classList.add('d-none');
        }
    }

    const savedTheme = localStorage.getItem('portfolio-theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    applyTheme(savedTheme || (prefersDark ? 'dark' : 'light'));

    if (toggleBtn) {
        toggleBtn.addEventListener('click', function () {
            const current = root.getAttribute('data-bs-theme');
            const next = current === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem('portfolio-theme', next);
        });
    }
})();
