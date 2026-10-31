/* Navegação progressiva para a listagem Quarto do blog na página inicial. */
(() => {
  const init = () => {
    const root = document.getElementById('home-blog-listing');
    const prev = document.getElementById('blog-prev');
    const next = document.getElementById('blog-next');
    if (!root || !prev || !next) return;
    const track = root.querySelector('.list.grid');
    if (!track) return;
    track.classList.add('js-blog-carousel');
    const update = () => {
      const max = Math.max(0, track.scrollWidth - track.clientWidth);
      const multiple = max > 4;
      prev.hidden = !multiple;
      next.hidden = !multiple;
      prev.disabled = !multiple || track.scrollLeft <= 4;
      next.disabled = !multiple || track.scrollLeft >= max - 4;
    };
    const slide = (direction) => {
      const item = track.firstElementChild;
      const gap = parseFloat(window.getComputedStyle(track).columnGap) || 16;
      const amount = (item ? item.getBoundingClientRect().width + gap : track.clientWidth) * direction;
      const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      track.scrollBy({left: amount, behavior: reducedMotion ? 'instant' : 'smooth'});
    };
    prev.addEventListener('click', () => slide(-1));
    next.addEventListener('click', () => slide(1));
    track.addEventListener('scroll', update, {passive: true});
    window.addEventListener('resize', update, {passive: true});
    window.addEventListener('load', update, {once: true});
    requestAnimationFrame(update);
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once: true});
  else init();
})();
