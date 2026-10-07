# Student-Panel Redesign — Task Checklist

Driven by `idea.txt` + 5 Dribbble refs (1 NeuroBank, 2 Borea/Environmental glass,
3 CyFocus, 4 Data-Viz, 5 Outcrowd). Comprehensive look overhaul applied everywhere relevant.

**Progress convention:** the master list lives here. After each *bunch* (workstream)
is finished and verified, a snapshot copy is saved as `REDESIGN_TASKS_<bunch>.md`
with those items ticked, so there's a record at every checkpoint.

> **Snapshot: B complete** (verified — lint clean, server 106 pass, client 110 pass, build OK, previewed in browser). A + D already complete (see `REDESIGN_TASKS_A-D.md`).

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
- [ ] New self-hosted font family (CSP 'self') — proposed at start.
- [ ] Rework size/weight hierarchy; big bold KPI numerals.
- [ ] Apply app-wide.

## D — Motion overhaul (refs 3, 4, 1)
- [x] Slow **all** motion to ~300–550ms calm ease-out; nothing fast.
- [x] Re-pace count-ups to match.
- [x] Keep the reduced-motion kill-switch.

## E — Page/route transitions (ref 4)
- [ ] Outgoing view shrinks/collapses/fades out as the new page takes its place — slow, morph-like, route-to-route.

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

## Notes on B (Cobalt & Crimson)

- Unlike the four earlier palettes (gradebook/midnight/ember/meadow, which recolor
  *all* neutrals), Cobalt & Crimson follow the **CyFocus concept**: they keep the
  neutral grey/charcoal base and only re-hue the accent + the top-edge glow.
- **Cobalt** (palette "5"): charcoal shell (base neutrals fall through), cool-blue
  brand — `#1d6fe0` light / `#4f9df7` dark.
- **Crimson** (palette "4"): a darker **near-black** shell (dark + system variants
  override surfaces below the base charcoal) with a crimson-red brand — `#d21f3c`
  light / `#f2555a` dark.
- Touch points: `client/src/lib/theme.js` + `server/src/lib/preferences.js`
  (enum — server rejects unknown palette on save), `client/src/index.css`
  (light + dark + system-dark token blocks), `client/src/pages/PreferencesPage.jsx`
  (two new swatches; the stale warm "Amber" aurora swatch was corrected to grey
  "Aurora"). `--brand-2` is set per palette so the login glow doesn't leak amber.
