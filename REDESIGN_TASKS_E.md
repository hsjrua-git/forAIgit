# Student-Panel Redesign — Task Checklist

Driven by `idea.txt` + 5 Dribbble refs (1 NeuroBank, 2 Borea/Environmental glass,
3 CyFocus, 4 Data-Viz, 5 Outcrowd). Comprehensive look overhaul applied everywhere relevant.

**Progress convention:** the master list lives here. After each *bunch* (workstream)
is finished and verified, a snapshot copy is saved as `REDESIGN_TASKS_<bunch>.md`
with those items ticked, so there's a record at every checkpoint.

## Confirmed decisions
- Font: designer's choice, proposed at start of C (easy to swap).
- Transparency slider: ~55% (see-through) → ~90% (nearly solid), middle default.
- Palette "4" = crimson-red · Palette "5" = cool-blue.
- Custom cursor: desktop/pointer only; off for touch and reduced-motion.

---

## A — Color rework (ref 3 + overall)
- [x] Neutral **grey** base (dark + light), not warm-brown.
- [x] **Top-edge ambient glow**, hue driven by the active palette.
- [x] Orange demoted to **accent + glow only**.

## B — New palettes (ref 5)
- [x] "5" charcoal + cool-blue accent/glow (light + dark) → **Cobalt**.
- [x] "4" near-black + crimson-red accent/glow (light + dark) → **Crimson**.
- [x] Each drives the top-glow hue; add swatches/labels to Preferences.

## C — Typography (overall)
- [x] New self-hosted font family (CSP 'self') → **Manrope** (variable, latin, 200–800).
- [x] Rework size/weight hierarchy; big bold KPI numerals (`.stat-value` 2.7rem/800, tabular).
- [x] Apply app-wide (set on `:root` via `--font`; everything inherits).

## D — Motion overhaul (refs 3, 4, 1)
- [x] Slow **all** motion to ~300–550ms calm ease-out; nothing fast.
- [x] Re-pace count-ups to match.
- [x] Keep the reduced-motion kill-switch.

## E — Page/route transitions (ref 4)
- [x] Outgoing view shrinks/collapses/fades out as the new page takes its place — slow, morph-like, route-to-route.

## F — Sidebar (ref 5)
- [ ] Collapse/expand toggle **at the top**, replacing the orange square.
- [ ] Collapsed icons **centered vertically**.
- [ ] **Collapsed by default at login.**
- [ ] **Sign out + Preferences pinned at the bottom** in both modes.

## G — Glassmorphism (ref 2, no moving background)
- [ ] Selective frosted glass on cards, topbar, popovers (backdrop-blur, hairline borders, layered depth).
- [ ] Static blackish/whitish backdrop — no motion.
- [ ] **Transparency slider** preference (saved server + client, wired to a CSS variable).

## H — Pop-ups (ref 3)
- [ ] Translucent, blurred **popovers** wherever they fit (menus, confirmations, pickers, tooltips).

## I — Custom cursor (ref 3)
- [ ] Glowing-dot cursor; **shrinks then springs back on click**; pointer-only; respects reduced-motion.

## J — Layout & content (ref 1 + overall)
- [ ] Dashboard → **bento grid** adapted to this app's data.
- [ ] Redesign **buttons** app-wide.
- [ ] Redesign **form fields/inputs** app-wide.
- [ ] Fix **placements, spacing, hierarchy** app-wide.
- [ ] (Optional) Slowed NeuroBank theme-toggle radial wipe.

---

## ✅ Done so far — may revisit later

### A — Color rework (done 2026-09-24, verified: lint · 110/110 tests · build)
- [x] Neutral **grey** base (dark + light), not warm-brown.
- [x] **Top-edge ambient glow**, hue driven by the active palette.
- [x] Orange demoted to **accent + glow only**.

### D — Motion overhaul (done 2026-09-24, verified: lint · 110/110 tests · build)
- [x] Slow **all** motion to ~300–550ms calm ease-out; nothing fast.
- [x] Re-pace count-ups to match.
- [x] Keep the reduced-motion kill-switch.

**Notes / possible revisits:**
- The top-edge glow is **already app-wide** (on the `body` canvas — every page sits on it), but reads *subtly* on interior pages: it's tuned fainter than login's and the topbar covers the strongest part of the edge. **Follow-up:** when the topbar becomes frosted glass in **G**, let the glow bleed through it so interior pages read as clearly as login. (Can also just raise `--glow-1/-2` if you want it stronger sooner.)
- Motion currently: `--t-fast: 320ms`, `--t: 480ms`, ease `cubic-bezier(0.33,1,0.68,1)`; CountUp default 1400ms. Easy to dial up/down from the tokens if the pace feels off anywhere.

### B — New palettes (done 2026-09-24, verified: lint · server 106 pass · client 110 pass · build · browser)
- [x] **Cobalt** (palette "5") — charcoal shell + cool-blue accent/glow (light + dark + system).
- [x] **Crimson** (palette "4") — near-black shell + crimson-red accent/glow (light + dark + system).
- [x] Both drive the top-edge glow hue; swatches + labels added to Preferences (stale "Amber" swatch also corrected to grey **Aurora**).

**Notes / possible revisits:**
- Unlike the four earlier palettes (gradebook/midnight/ember/meadow, which recolor *all* neutrals), Cobalt & Crimson follow the CyFocus concept: they **keep the neutral grey/charcoal base** and only re-hue `--brand` / `--brand-strong` / `--brand-2`. Cobalt lets the base charcoal fall through in dark mode; Crimson overrides to a darker near-black shell. The `:root[data-palette]` common block auto-derives `--glow-2`, `--sidebar-active-*`, `--brand-soft` from `--brand`; `--brand-2` is set per palette so the login glow doesn't leak amber.
- Names 'cobalt'/'crimson' are wired into `client/src/lib/theme.js` **and** `server/src/lib/preferences.js` (the server enum rejects unknown palette values on save).

### C — Typography (done 2026-09-24, verified: lint · client 110 pass · build · browser font-load confirmed)
- [x] **Manrope**, self-hosted variable woff2 (latin, weight axis 200–800) → `client/src/assets/fonts/manrope-variable.woff2`, one `@font-face` at top of index.css, `font-display: swap`. Emitted by Vite from our own origin → satisfies `font-src 'self'` (no external requests, LAN-safe).
- [x] Reworked hierarchy: `--font` / `--font-numeric` tokens on `:root` (whole app inherits); headings bolder + tighter (h1 1.7rem/750, h2 1.2rem/700, h3 1rem/680, tracking -0.02em); auth title 1.75rem/750.
- [x] Big bold KPI numerals: `.stat-value` 2rem/700 → **2.7rem/800**, tighter tracking, `tabular-nums lining-nums`.

**Notes / possible revisits:**
- Font choice was mine per the plan (Manrope: geometric, modern-dashboard character matching the NeuroBank/CyFocus refs, strong heavy weights for KPIs, clean at small sizes for tables). **Easy to swap** — replace the one woff2 + the `@font-face`/`--font` tokens. If you'd prefer more character (e.g. Space Grotesk for numerals) or the safe default (Inter), say so.
- Existing fractional weights (680/640/560…) carry over fine — Manrope's variable axis is continuous. Monospace (code/audit meta) left on the system `ui-monospace` stack intentionally.
- CSP already had `fontSrc: ["'self'"]` in `server/src/index.js`, so no server change was needed.

### E — Page/route transitions (done 2026-09-24, verified: lint · 110/110 tests · build · browser console clean)
- [x] Route-to-route **View Transitions** morph: outgoing page settles out (fade + slight downward drift + scale-to-0.985 over 300ms) while the incoming page rises in (fade up + scale from 0.99 over `--t` 480ms), driven for **every** navigation (sidebar link, account menu, programmatic redirect), with the shell (sidebar/topbar) held still.

**Notes / possible revisits:**
- Implemented as a **global** driver in `client/src/App.jsx` (`AnimatedRoutes`): pins `<Routes location={displayed}>` to a "displayed" location and only advances it inside `document.startViewTransition(...)`, so the routed region morphs while unchanged chrome stays put. Chose this over per-`<Link viewTransition>` props so it covers all navigation types with one contained change.
- Only `#main-content` is named (`view-transition-name: page` in index.css, gated by `@supports (view-transition-name: none)`); the remount `page-enter` animation is disabled on VT-capable browsers so it doesn't stack with `::view-transition-new`.
- Reduced-motion / no-API path advances the location in the render phase (guarded self-limiting setState — the same pattern Layout uses) for an instant swap; CSS also disables the VT animations under `prefers-reduced-motion`.
- Robustness: dedupe by `location.key` so StrictMode's dev double-invoke starts exactly one transition per navigation; `skipTransition()` on the prior transition for rapid re-navigation; no-op `.catch()` on `ready`/`updateCallbackDone`/`finished` so an aborted/superseded transition's promise rejections don't surface as uncaught (this was the earlier `InvalidStateError` console noise — now gone; verified in a fresh tab across normal and rapid back-to-back navigations).
- Context7 was unreachable this session; relied on established knowledge of the View Transitions API and react-router's `location` prop.
