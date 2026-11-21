# SchemeFinder Design Specification: Civic Parchment & Forest

## 1. Visual Direction & Mood
- **Archetype**: Civic Parchment & Forest (Direction 1).
- **Tone**: Grounded, official, reassuring, unhurried civic clarity. Built for trust at the last mile (citizens, rural families, and Common Service Centre / VLE operators).
- **Metaphor**: *"The Civic Ledger Unfolding"* — a physical-feeling civic passbook replacing bureaucratic anxiety with deterministic, dignified entitlement verification.

---

## 2. Color Palette & CSS Variables
Strict contrast rules: Bronze/Gold (`--color-accent`) is **never** used for body text or small interactive labels. Deep Forest (`--color-forest`) is the authoritative primary color for text, heavy surfaces, and primary buttons.

```css
:root {
  /* Dominant / Authoritative Dark */
  --color-forest: #11302A;           /* Primary text, solid buttons, dark panels */
  --color-forest-dark: #0A1F1B;      /* Deep contrast hover, footer background */
  --color-forest-soft: #1E4D44;      /* Secondary dark accents, subtle badges */

  /* Parchment Neutrals (Warm, paper-like, glare-free) */
  --color-parchment: #F7F4EB;        /* Primary page canvas */
  --color-parchment-card: #FFFFFF;   /* Foreground card surface */
  --color-parchment-muted: #EFECE1;  /* Inset wells, step backdrops, form inputs */
  --color-border: #D8D3C5;           /* Structural borders, perforated dividers */
  --color-border-dark: #B5AD9B;      /* Focused input borders, card frames */

  /* Ashoka Bronze / Ochre (Warm civic accent) */
  --color-accent: #C88A2C;           /* Seals, progress fills, decorative trim ONLY */
  --color-accent-light: #FDF3E3;     /* Highlight background tints */
  --color-accent-dark: #9B651B;      /* High-contrast border highlights */

  /* Semantics (Deterministic Scheme Statuses) */
  --status-eligible-bg: #E8F5E9;
  --status-eligible-text: #1B5E20;
  --status-eligible-border: #81C784;

  --status-almost-bg: #FFF8E1;
  --status-almost-text: #B76E00;
  --status-almost-border: #FFD54F;

  --status-missing-bg: #FFEBEE;
  --status-missing-text: #B71C1C;
  --status-missing-border: #EF9A9A;
}
```

---

## 3. Typography
Maximum three font families, vendored locally in `static/vendor/fonts/`:
1. **Display / Headings**: `Fraunces` (Serif, variable / 600-700) — Dignified civic editorial weight, authoritative yet humane.
2. **Body & Controls (English)**: `Plus Jakarta Sans` (Sans, 400, 500, 600) — High x-height, wide apertures, legible on cheap 390px mobile screens under direct sunlight.
3. **Indic Script (Hindi)**: `Noto Sans Devanagari` (400, 600) — Pristine Devanagari legibility matched to Latin body metrics.

Font sizes maintain strict scale contrast (Hero 2.5rem–3.25rem, Section 1.75rem, Card Title 1.25rem, Body 1rem, Caption 0.875rem).

---

## 4. Signature Elements (CSS-Only)
1. **Perforated Passbook Border (`.passbook-edge`)**:
   - Built with pure CSS radial-gradient punch holes along card dividers, evoking physical government ration cards and passbooks.
2. **Seal of Eligibility (`.civic-stamp`)**:
   - Circular rotated badge with double concentric border and uppercase monospace/serif text (`ELIGIBLE NOW` / `पात्रता प्रमाणित`), angled at -6deg to mimic physical rubber stamps.
3. **Tactile High-Contrast Controls**:
   - Oversized radio pills (minimum 52px height) and bold checkbox tiles with thick 2px borders, large feedback checkmarks, and 0.15s spring transform.

---

## 5. Mobile-First & Accessibility Constraints
- **Tap Targets**: Every clickable element (HTMX wizard step choice, document toggle, language pill) has a minimum touch footprint of 48px × 48px.
- **Sunlight Readability**: Contrast ratio of all text against parchment exceeds 7.5:1 (Forest `#11302A` on `#F7F4EB` = 12.8:1).
- **Offline / Local Guarantee**: Zero external font or script CDN requests. All SVGs inline. Fully operational on disconnected networks.
- **Privacy Assurance**: Explicit badge stating: *"No login. No database. Stored in your browser session only."*
