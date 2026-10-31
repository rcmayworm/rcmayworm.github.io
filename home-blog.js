/* Vitrine horizontal dos artigos publicados na página inicial.
   Quarto mantém a listagem automática; esta camada controla apenas a navegação. */
(() => {
  const init = () => {
    const root = document.getElementById('home-blog-listing');
    const prev = document.getElementById('blog-prev');
    const next = document.getElementById('blog-next');
    if (!root || !prev || !next) return false;

    const track = root.matches('.list.grid') ? root : root.querySelector('.list.grid');
    if (!track) return false;
    if (track.dataset.carouselInitialized === 'true') return true;
    track.dataset.carouselInitialized = 'true';
    track.classList.add('js-blog-carousel');
    track.tabIndex = 0;
    track.setAttribute('role', 'region');
    track.setAttribute('aria-label', 'Artigos do blog: use as setas para navegar horizontalmente');

    const update = () => {
      const max = Math.max(0, track.scrollWidth - track.clientWidth);
      const canSlide = max > 4;
      prev.hidden = !canSlide;
      next.hidden = !canSlide;
      prev.disabled = !canSlide || track.scrollLeft <= 4;
      next.disabled = !canSlide || track.scrollLeft >= max - 4;
    };

    const slide = (direction) => {
      const item = track.firstElementChild;
      if (!item) return;
      const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      const stride = item.getBoundingClientRect().width + gap;
      const max = Math.max(0, track.scrollWidth - track.clientWidth);
      const current = Math.round(track.scrollLeft / stride);
      const target = Math.min(max, Math.max(0, (current + direction) * stride));
      const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
      track.scrollTo({left: target, behavior: reduced ? 'auto' : 'smooth'});
    };

    prev.addEventListener('click', () => slide(-1));
    next.addEventListener('click', () => slide(1));
    track.addEventListener('scroll', update, {passive: true});
    window.addEventListener('resize', update, {passive: true});
    window.addEventListener('load', update, {once: true});
    if ('ResizeObserver' in window) new ResizeObserver(update).observe(track);
    requestAnimationFrame(update);
    return true;
  };

  const start = () => {
    if (init()) return;
    // Segurança caso uma versão do Quarto insira a listagem após DOMContentLoaded.
    const observer = new MutationObserver(() => {
      if (init()) observer.disconnect();
    });
    observer.observe(document.body, {childList: true, subtree: true});
    window.addEventListener('load', () => {
      if (init()) observer.disconnect();
    }, {once: true});
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start, {once: true});
  else start();
})();
