import { useEffect, useRef, useState } from 'react';

// Workstream I — the glowing-dot cursor (reference 3 / CyFocus).
//
// A two-layer pointer: a crisp core dot that tracks the mouse exactly, and a
// softer ring that lags a touch behind it (the one "comet" flourish, kept gentle
// to match the app-wide calm motion). It shrinks and springs back on click,
// swells over actionable elements, and — the Hybrid decision — steps aside over
// text fields so the native caret stays precise in this data-entry-heavy app.
//
// It exists only for a true desktop mouse (a fine, hovering pointer) and never
// under reduced motion. The paint lives in index.css (the `.cursor-*` section);
// this file is the gate + the machinery.

// Live gate. Mirrors the matchMedia-subscription pattern in CountUp.jsx so a
// mid-session change — plugging in a mouse, toggling the OS reduced-motion
// setting — is picked up and the cursor mounts or unmounts accordingly.
function useCursorEnabled() {
  const evaluate = () =>
    typeof window !== 'undefined' &&
    typeof window.matchMedia === 'function' &&
    window.matchMedia('(pointer: fine)').matches &&
    window.matchMedia('(hover: hover)').matches &&
    !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const [enabled, setEnabled] = useState(evaluate);

  useEffect(() => {
    const queries = [
      window.matchMedia('(pointer: fine)'),
      window.matchMedia('(hover: hover)'),
      window.matchMedia('(prefers-reduced-motion: reduce)'),
    ];
    const update = () => setEnabled(evaluate());
    queries.forEach((q) => q.addEventListener('change', update));
    return () => queries.forEach((q) => q.removeEventListener('change', update));
  }, []);

  return enabled;
}

// Elements the ring should swell over (actionable) vs. text fields where we get
// out of the way and let the native caret show.
const CLICK_SELECTOR =
  'a[href], button, summary, label, select, [role="button"], .btn, ' +
  'input[type="button"], input[type="submit"], input[type="reset"], ' +
  'input[type="checkbox"], input[type="radio"], [data-cursor="interactive"]';
const TEXT_SELECTOR =
  'input:not([type="button"]):not([type="submit"]):not([type="reset"])' +
  ':not([type="checkbox"]):not([type="radio"]):not([type="range"])' +
  ':not([type="color"]):not([type="file"]):not([type="image"]):not([type="hidden"]), ' +
  'textarea, [contenteditable="true"], [contenteditable=""]';

function Cursor() {
  const layerRef = useRef(null);
  const dotRef = useRef(null);
  const ringRef = useRef(null);

  useEffect(() => {
    const layer = layerRef.current;
    const dot = dotRef.current;
    const ring = ringRef.current;
    if (!layer || !dot || !ring) return undefined;

    // Hides the native cursor (see the CSS `html.cursor-active` rule) only while
    // this layer is actually live, so a signed-off JS layer never leaves the page
    // without a visible pointer.
    const root = document.documentElement;
    root.classList.add('cursor-active');

    let targetX = 0;
    let targetY = 0;
    let ringX = 0;
    let ringY = 0;
    let placed = false;
    let visible = false;
    let rafId = 0;

    // The ring eases toward the pointer a fraction each frame; once it has caught
    // up we snap and stop the loop, so there's no perpetual rAF while idle.
    const drawRing = () => {
      rafId = 0;
      const dx = targetX - ringX;
      const dy = targetY - ringY;
      if (Math.abs(dx) < 0.4 && Math.abs(dy) < 0.4) {
        ringX = targetX;
        ringY = targetY;
      } else {
        ringX += dx * 0.18;
        ringY += dy * 0.18;
      }
      ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0)`;
      if (ringX !== targetX || ringY !== targetY) {
        rafId = requestAnimationFrame(drawRing);
      }
    };

    const onMove = (e) => {
      targetX = e.clientX;
      targetY = e.clientY;
      dot.style.transform = `translate3d(${targetX}px, ${targetY}px, 0)`;
      if (!placed) {
        // First sighting: drop the ring straight onto the pointer instead of
        // letting it swoop in from the top-left origin.
        ringX = targetX;
        ringY = targetY;
        ring.style.transform = `translate3d(${ringX}px, ${ringY}px, 0)`;
        placed = true;
      }
      if (!visible) {
        layer.classList.add('is-visible');
        visible = true;
      }
      if (!rafId) rafId = requestAnimationFrame(drawRing);
    };

    const onOver = (e) => {
      const t = e.target;
      if (!(t instanceof Element)) return;
      const overText = Boolean(t.closest(TEXT_SELECTOR));
      layer.classList.toggle('is-text', overText);
      layer.classList.toggle(
        'is-interactive',
        !overText && Boolean(t.closest(CLICK_SELECTOR)),
      );
    };

    const onDown = () => layer.classList.add('is-pressed');
    const onUp = () => layer.classList.remove('is-pressed');

    const hide = () => {
      layer.classList.remove('is-visible');
      visible = false;
    };
    // relatedTarget null on pointerout means the pointer left the window entirely.
    const onOut = (e) => {
      if (!e.relatedTarget) hide();
    };

    window.addEventListener('pointermove', onMove, { passive: true });
    window.addEventListener('pointerover', onOver, { passive: true });
    window.addEventListener('pointerdown', onDown, { passive: true });
    window.addEventListener('pointerup', onUp, { passive: true });
    window.addEventListener('pointerout', onOut, { passive: true });
    window.addEventListener('blur', hide);

    return () => {
      window.removeEventListener('pointermove', onMove);
      window.removeEventListener('pointerover', onOver);
      window.removeEventListener('pointerdown', onDown);
      window.removeEventListener('pointerup', onUp);
      window.removeEventListener('pointerout', onOut);
      window.removeEventListener('blur', hide);
      if (rafId) cancelAnimationFrame(rafId);
      root.classList.remove('cursor-active');
    };
  }, []);

  return (
    <div className="cursor-layer" ref={layerRef} aria-hidden="true">
      <div className="cursor-ring" ref={ringRef}>
        <i />
      </div>
      <div className="cursor-dot" ref={dotRef}>
        <i />
      </div>
    </div>
  );
}

export default function CustomCursor() {
  const enabled = useCursorEnabled();
  return enabled ? <Cursor /> : null;
}
