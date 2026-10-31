/* Carrossel de postagens na home. Localiza a listagem mesmo após Quarto
   renomear o contêiner para #listing-home-blog-listing. */
(() => {
  const candidates = [
    '#listing-home-blog-listing .quarto-listing-grid',
    '#listing-home-blog-listing .list.grid',
    '#home-blog-listing .quarto-listing-grid',
    '#home-blog-listing .list.grid',
    '#listing-home-blog-listing.list.grid',
    '#home-blog-listing.list.grid',
    'body:has(.academic-hero) .quarto-listing-grid'
  ];
  const init = () => {
    const prev = document.getElementById('blog-prev');
    const next = document.getElementById('blog-next');
    if (!prev || !next) return false;
    const tracks = document.querySelectorAll(candidates.join(','));
    const track = [...tracks].find(el => el.querySelector('a[href*="blog/posts/"]'));
    if (!track) return false;
    if (track.dataset.carouselInitialized === 'true') return true;
    track.dataset.carouselInitialized = 'true';
    track.classList.add('js-blog-carousel');
    if (!track.id) track.id = 'home-blog-carousel-track';
    prev.setAttribute('aria-controls', track.id);
    next.setAttribute('aria-controls', track.id);
    track.tabIndex = 0;
    track.setAttribute('role', 'region');
    track.setAttribute('aria-label', 'Artigos do blog: navegação horizontal');

    const update = () => {
      const max = Math.max(0, track.scrollWidth - track.clientWidth);
      const overflow = max > 4;
      prev.hidden = !overflow;
      next.hidden = !overflow;
      prev.disabled = !overflow || track.scrollLeft <= 4;
      next.disabled = !overflow || track.scrollLeft >= max - 4;
    };
    const slide = direction => {
      const first = track.firstElementChild;
      if (!first) return;
      const gap = parseFloat(getComputedStyle(track).columnGap) || 0;
      const stride = first.getBoundingClientRect().width + gap;
      const max = Math.max(0, track.scrollWidth - track.clientWidth);
      const step = Math.round(track.scrollLeft / stride) + direction;
      const destination = Math.max(0, Math.min(max, step * stride));
      const behavior = matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth';
      track.scrollTo({left: destination, behavior});
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
