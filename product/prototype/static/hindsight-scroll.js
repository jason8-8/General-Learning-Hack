'use strict';
(() => {
  // Keep this layer independent of the 3D head's future controls and renderer.
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const app = window.ScrollCraft ? ScrollCraft.mount(document) : null;
  function syncReceipt() {
    if (typeof study === 'undefined' || !study) return;
    const current = currentScenario();
    document.getElementById('trail-audience').textContent = current.segment;
    document.getElementById('trail-price').textContent = `£${current.price_gbp_per_trip} / trip`;
    document.getElementById('trail-baseline').textContent = frozenBaseline
      ? `Saved: £${frozenBaseline.price_gbp_per_trip} · ${frozenBaseline.concept === 'basic' ? 'basic itinerary' : 'readiness pack'}`
      : 'No frozen baseline yet';
    document.querySelector('.trail-receipt').dataset.frozen = String(Boolean(frozenBaseline));
  }
  let queued = false;
  function queueSync() {
    if (queued) return;
    queued = true;
    requestAnimationFrame(() => {queued = false; syncReceipt();});
  }
  ['click', 'input', 'change'].forEach(name => document.addEventListener(name, queueSync));
  new MutationObserver(() => {queueSync(); if(app) app.layout();}).observe(document.getElementById('paid-count'), {childList:true});
  window.addEventListener('load', () => {syncReceipt(); if(app) app.layout();});
  // Always reveal headings if motion preference changes after initial load.
  motion.addEventListener('change', () => {
    document.querySelectorAll('[data-sc-in]').forEach(el => el.classList.add('sc-in'));
  });
  syncReceipt();
})();
