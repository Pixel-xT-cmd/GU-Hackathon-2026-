/* SchemeFinder Client Interactivity & Motion (Offline Local) */
document.addEventListener('DOMContentLoaded', () => {
  // GSAP animations if GSAP is available and user doesn't prefer reduced motion
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (window.gsap && !prefersReducedMotion) {
    // Gentle reveal for hero elements
    gsap.from('.hero-title', {
      opacity: 0,
      y: 16,
      duration: 0.8,
      ease: 'power3.out'
    });
    gsap.from('.hero-subtitle', {
      opacity: 0,
      y: 12,
      duration: 0.8,
      delay: 0.2,
      ease: 'power3.out'
    });
    gsap.from('.passbook-card', {
      opacity: 0,
      y: 20,
      duration: 0.7,
      delay: 0.35,
      ease: 'power3.out'
    });
  }

  // HTMX animation hook on swap
  document.body.addEventListener('htmx:afterSwap', (evt) => {
    if (window.gsap && !prefersReducedMotion) {
      const target = evt.detail.target;
      if (target) {
        gsap.from(target.querySelectorAll('.scheme-card, .civic-stamp, .readiness-meter'), {
          opacity: 0,
          y: 10,
          stagger: 0.08,
          duration: 0.5,
          ease: 'power2.out'
        });
      }
    }
  });
});