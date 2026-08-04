# TruthShield X — Design System & UI/UX Guidelines
## Document: 05-Design.md
**Version:** 2.0 (Expert-Reviewed Master Design System)  
**Status:** Approved Technical Specification & UI Standard  
**Target Platform:** Web (React 19 + Tailwind CSS), Android (Jetpack Compose), Extension (Manifest V3)  
**Design Philosophy:** Premium Government + Enterprise AI Cyber SaaS (Dark-Mode First, Glassmorphic, Accessible, Colorblind-Safe)

---

# Changelog from v1.0
- Added colorblind-safe redundancy rules for the Trust Score matrix
- Added elevation/z-index scale
- Added form input state specs (error/disabled/focus/success)
- Added responsive breakpoint table
- Added `prefers-reduced-motion` accessibility rule
- Added data visualization / chart color rules
- Added multilingual typography (Devanagari support)
- Added design-to-dev token handoff spec
- Added component states matrix (hover/active/disabled/loading for buttons)

---

# Table of Contents

1. Executive Design Philosophy & Brand Identity
2. Core Design Principles
3. Color Palette & HSL Design Tokens
4. Digital Trust Score Matrix & Colorblind-Safe Mapping
5. Typography Scale & Multilingual Support
6. Design Tokens & CSS Variables Blueprint
7. Layout Grid, Spacing, Breakpoints & Elevation
8. Glassmorphism Tokens
9. Component Architecture & UI Anatomy
10. Form & Input States
11. Navigation System
12. Iconography & Visual Assets
13. Data Visualization & Chart Color Rules
14. Micro-Animations & Motion Design (with Reduced-Motion Support)
15. Loading, Skeleton & Empty States
16. Accessibility (WCAG 2.1 AA) & Keyboard Navigation
17. Dark & Light Mode Support
18. Design-to-Dev Handoff & Token Governance
19. UI Quality Assurance Sign-Off Checklist

---

# 1. Executive Design Philosophy & Brand Identity

TruthShield X combines the authoritative credibility of a **Government Cyber Defense Agency** with the sleek innovation of an **Enterprise AI SaaS Platform**.

**Brand Attributes:** Authoritative, Intelligent, Transparent, Secure, Minimalist, High-Tech.  
**Visual Aesthetic:** Deep Charcoal/Slate background, Electric Cyan highlights, Glassmorphic frosted-glass containers, vibrant *and redundant* semantic status indicators (never color-only).

---

# 2. Core Design Principles

1. **Trust & Security First** — every screen communicates authenticity, transparent AI reasoning, and data protection.
2. **Zero Technical Jargon** — complex AI inferences translated into clear citizen guidance.
3. **Explainability by Default** — no score without headline, confidence, evidence, and recommendation.
4. **Single-Objective Simplicity** — one primary CTA per viewport.
5. **Universal Accessibility** — WCAG 2.1 AA, colorblind-safe, full keyboard support, reduced-motion support.
6. **Never Color-Alone** — every status signal pairs color with an icon, shape, or text label. This is a security product; a red-green colorblind user misreading "Trusted" as "Dangerous" is a real failure mode, not an edge case.

---

# 3. Color Palette & HSL Design Tokens

| Color Name | Hex Code | HSL Value | Usage Role |
|---|---|---|---|
| **Background Dark** | `#020617` | `hsl(222, 84%, 5%)` | Primary Application Canvas |
| **Card Surface** | `#0F172A` | `hsl(222, 47%, 11%)` | Primary Container Background |
| **Surface Hover** | `#1E293B` | `hsl(217, 33%, 17%)` | Card & Row Hover State |
| **Border Dark** | `#334155` | `hsl(215, 25%, 27%)` | Borders & Dividers |
| **Accent Cyan** | `#06B6D4` | `hsl(189, 94%, 43%)` | Primary Buttons, Active States |
| **Accent Blue** | `#3B82F6` | `hsl(217, 91%, 60%)` | Secondary Actions & Links |
| **Text Primary** | `#F8FAFC` | `hsl(210, 40%, 98%)` | Headings & Body Text |
| **Text Muted** | `#94A3B8` | `hsl(215, 16%, 65%)` | Subtitles, Captions |
| **Status Green** | `#10B981` | `hsl(160, 84%, 39%)` | Trusted / Success |
| **Status Amber** | `#F59E0B` | `hsl(38, 92%, 50%)` | Medium Risk |
| **Status Red** | `#EF4444` | `hsl(0, 84%, 60%)` | Dangerous / Critical |

---

# 4. Digital Trust Score Matrix & Colorblind-Safe Mapping

Color alone is insufficient — roughly 8% of men and 0.5% of women have color vision deficiency, and red/amber/orange are the hardest hues to distinguish for the most common type (deuteranopia). Every tier below MUST pair color with a distinct **icon + shape + text label**, not color alone.

| Score | Status | Hex | Icon | Shape Signal | Pattern (charts only) |
|---|---|---|---|---|---|
| 90–100 | `TRUSTED` | `#10B981` | ShieldCheck | Solid filled ring | Solid fill |
| 70–89 | `LOW RISK` | `#3B82F6` | ShieldQuestion | Ring, 3/4 filled | Diagonal stripes |
| 50–69 | `MEDIUM RISK` | `#F59E0B` | ShieldAlert | Ring, 1/2 filled | Dots |
| 30–49 | `HIGH RISK` | `#F97316` | AlertTriangle | Ring, 1/4 filled | Cross-hatch |
| 0–29 | `DANGEROUS` | `#EF4444` | ShieldX | Ring, near-empty + pulse | Dense hatch |

**Rule:** Status badges always render as `[icon] LABEL` — never a bare color chip. Verify against a deuteranopia simulator (e.g., Stark/Coblis) before sign-off.

---

# 5. Typography Scale & Multilingual Support

## Primary Typeface: Inter (Latin script)

| Level | Size | Weight | Line Height | CSS Utility |
|---|---|---|---|---|
| Hero Display | 48px | Bold (700) | 1.1 | `text-5xl font-bold tracking-tight` |
| H1 Headline | 36px | Bold (700) | 1.2 | `text-4xl font-bold tracking-tight` |
| H2 Section | 30px | SemiBold (600) | 1.25 | `text-3xl font-semibold` |
| H3 Subsection | 24px | SemiBold (600) | 1.3 | `text-2xl font-semibold` |
| H4 Component | 20px | Medium (500) | 1.4 | `text-xl font-medium` |
| Body Primary | 16px | Regular (400) | 1.5 | `text-base font-normal` |
| Body Small | 14px | Regular (400) | 1.5 | `text-sm font-normal` |
| Caption/Meta | 12px | Medium (500) | 1.4 | `text-xs font-medium uppercase` |

## Multilingual / Devanagari Support
Inter does not render Hindi/Devanagari script. For an India-wide product this is a real requirement, not optional polish:
- **Devanagari pairing font:** `Noto Sans Devanagari` — loaded conditionally when `lang="hi"`
- **Font stack:** `font-family: 'Inter', 'Noto Sans Devanagari', sans-serif;`
- Line-height increases by 10% for Devanagari (`1.5` → `1.65`) since conjunct characters need more vertical breathing room
- All XAI evidence text and CTA labels must exist in an i18n key file (`en.json` / `hi.json`) from day one — retrofitting translation later is expensive

---

# 6. Design Tokens & CSS Variables Blueprint

```css
@layer base {
  :root {
    --background: 222 84% 5%;
    --foreground: 210 40% 98%;
    --card: 222 47% 11%;
    --card-foreground: 210 40% 98%;
    --popover: 222 47% 11%;
    --popover-foreground: 210 40% 98%;
    --primary: 189 94% 43%;
    --primary-foreground: 222 47% 11%;
    --secondary: 217 33% 17%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217 33% 17%;
    --muted-foreground: 215 16% 65%;
    --accent: 189 94% 43%;
    --accent-foreground: 222 47% 11%;
    --destructive: 0 84% 60%;
    --destructive-foreground: 210 40% 98%;
    --success: 160 84% 39%;
    --warning: 38 92% 50%;
    --border: 215 25% 27%;
    --input: 215 25% 27%;
    --ring: 189 94% 43%;
    --radius: 0.75rem;
  }

  /* Reduced motion — see Section 14 */
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
      animation-duration: 0.01ms !important;
      animation-iteration-count: 1 !important;
      transition-duration: 0.01ms !important;
      scroll-behavior: auto !important;
    }
  }
}
```

---

# 7. Layout Grid, Spacing, Breakpoints & Elevation

## Spacing Scale (4px base grid)
`4px` `8px` `12px` `16px` `24px` `32px` `48px` `64px` → `space-1` through `space-16`

## Responsive Breakpoints

| Token | Min Width | Target Device |
|---|---|---|
| `xs` | 320px | Small mobile |
| `sm` | 640px | Large mobile |
| `md` | 768px | Tablet |
| `lg` | 1024px | Small desktop / sidebar visible |
| `xl` | 1280px | Standard desktop |
| `2xl` | 1440px | Max canvas width (centered beyond this) |

**Grid rule:** `grid-cols-1` below `md`, `grid-cols-6` at `md`, `grid-cols-12` at `lg` and above.

## Elevation / Z-Index Scale
Without this, glass cards, modals, and toasts collide unpredictably:

| Layer | z-index | Usage |
|---|---|---|
| Base content | `0` | Page content, cards |
| Sticky nav/sidebar | `10` | Fixed navigation |
| Dropdowns/tooltips | `20` | Select menus, tooltips |
| Modal overlay backdrop | `40` | Dimmed background |
| Modal/dialog | `50` | Modal content itself |
| Toast/notification | `60` | Always on top |

---

# 8. Glassmorphism Tokens

```css
.glass-card {
  background: rgba(15, 23, 42, 0.75);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid rgba(51, 65, 85, 0.5);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  border-radius: var(--radius);
}
```
**Performance note:** `backdrop-filter: blur()` is GPU-expensive on low-end Android devices. Cap simultaneous glass-card instances visible per viewport to ≤6, or fall back to solid `--card` background below a defined device tier.

---

# 9. Component Architecture & UI Anatomy

## 9.1 Unified Upload & Dropzone Component
Accepts files, URLs, text, and camera QR intake in a single unified box.

## 9.2 Radial Digital Trust Score Gauge

```tsx
export const TrustScoreGauge = ({ score, status }: { score: number; status: string }) => {
  const getColor = (s: number) => {
    if (s >= 90) return '#10B981';
    if (s >= 70) return '#3B82F6';
    if (s >= 50) return '#F59E0B';
    if (s >= 30) return '#F97316';
    return '#EF4444';
  };

  const color = getColor(score);

  return (
    <div className="flex flex-col items-center justify-center p-6 glass-card" role="img" aria-label={`Trust score ${score} out of 100, status ${status}`}>
      <div className="relative flex items-center justify-center w-36 h-36">
        <svg className="w-full h-full transform -rotate-90" viewBox="0 0 36 36">
          <path className="text-slate-800" strokeWidth="3.5" stroke="currentColor" fill="none"
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
          <path strokeDasharray={`${score}, 100`} stroke={color} strokeWidth="3.5" strokeLinecap="round" fill="none"
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
        </svg>
        <span className="absolute text-4xl font-bold text-white">{score}</span>
      </div>
      <span className="mt-4 px-3 py-1 rounded-full text-xs font-semibold uppercase tracking-wider text-white flex items-center gap-1.5" style={{ backgroundColor: color }}>
        {status}
      </span>
    </div>
  );
};
```
Note the added `role="img"` + `aria-label` — screen readers previously had no way to announce the score.

## 9.3 Explainable AI (XAI) Evidence Card
Displays bulleted evidence factors with severity badges (`CRITICAL`, `HIGH`, `MEDIUM`) — icon-paired per Section 4 rule, never color-only.

---

# 10. Form & Input States

| State | Border | Background | Notes |
|---|---|---|---|
| Default | `border-slate-600` | `bg-slate-900/50` | — |
| Hover | `border-cyan-500/50` | unchanged | 150ms transition |
| Focus | `border-cyan-500` + ring | unchanged | `ring-2 ring-cyan-500/40` |
| Filled | `border-slate-500` | unchanged | — |
| Error | `border-red-500` | `bg-red-500/5` | Pair with inline `AlertCircle` icon + text message below field, never color-only |
| Success | `border-green-500` | `bg-green-500/5` | Pair with `CheckCircle` icon |
| Disabled | `border-slate-800` | `bg-slate-900/30` | `opacity-50 cursor-not-allowed` |

**Button states:** `default / hover (scale 1.02) / active (scale 0.98) / disabled (opacity 40%, no pointer events) / loading (spinner replaces label, button width locked to prevent layout shift)`.

---

# 11. Navigation System

- **Desktop:** Collapsible left sidebar (240px expanded / 64px collapsed), dark glass background. Items: Dashboard, Unified Scanner, History, Analytics Map, Reports, Admin Panel.
- **Mobile:** Bottom fixed nav (64px height), 5 core icons: Home, Scan, History, Alerts, Profile.
- **Browser Extension Popup:** 360x500px compact view — current page Trust Score, instant scan trigger, threat toggle.

---

# 12. Iconography & Visual Assets

- **Icon Set:** Lucide React (`lucide-react`), stroke width `1.75px`, default size `20px` (`w-5 h-5`)
- **Icon size scale:** `16px` (inline/caption) / `20px` (default UI) / `24px` (nav/section headers) / `32px` (empty states/hero)
- **Core Icons:** `ShieldCheck`, `ShieldAlert`, `ShieldX`, `ScanLine`, `FileText`, `Video`, `QrCode`, `MapPin`

---

# 13. Data Visualization & Chart Color Rules

- **Categorical chart palette (max 6 series):** Cyan `#06B6D4`, Blue `#3B82F6`, Amber `#F59E0B`, Emerald `#10B981`, Violet `#8B5CF6`, Slate `#94A3B8` — chosen for pairwise distinguishability under deuteranopia simulation
- **Sequential/heatmap scale (single metric, e.g. threat density):** single-hue ramp from `#0F172A` (low) to `#06B6D4` (high) — never a rainbow scale, which misleads magnitude perception
- **Never** use a red-to-green single gradient for any chart — colorblind users lose the signal entirely; use red-to-amber-to-blue instead (matches the Trust Score matrix logic)
- All charts include data labels or a legend with icons — never rely on hover-only tooltips as the sole source of a value

---

# 14. Micro-Animations & Motion Design

Framer Motion for subtle, non-distracting feedback:
- **Page transitions:** fade + slight Y-slide (`opacity 0→1, y 10→0`, 250ms)
- **Button hover:** `whileHover={{ scale: 1.02 }}`, `whileTap={{ scale: 0.98 }}`
- **Scan progress:** smooth linear pulse ring around dropzone during analysis

**Reduced motion (required, not optional):** All animations must respect `prefers-reduced-motion`. See the CSS block in Section 6 — this is a WCAG 2.1 AA expectation, and vestibular-disorder users can experience real discomfort from unthrottled motion.

---

# 15. Loading, Skeleton & Empty States

- **Skeletons:** animated shimmer blocks (`bg-slate-800 animate-pulse rounded-md`) matching exact component dimensions — never a blank white screen
- **Empty states:** friendly illustration + explanation + primary CTA (e.g., "No scans recorded yet. Upload your first link or file to test system authenticity.")

---

# 16. Accessibility (WCAG 2.1 AA) & Keyboard Navigation

- Contrast ratio at least 4.5:1 for body text, at least 7:1 for headers
- Explicit focus rings on all interactive elements (`focus-visible:ring-2 focus-visible:ring-cyan-500 focus-visible:outline-none`)
- `aria-label` on all icon-only buttons
- All status/score components carry `role` + `aria-label` (see Section 9.2)
- Full keyboard tab order tested on every new page before merge
- Reduced-motion respected globally (Section 14)

---

# 17. Dark & Light Mode Support

Dark Mode is default. Light Mode fully supported via CSS variable overrides — components must always read color through semantic Tailwind classes (`bg-background text-foreground border-border`), never hardcoded hex values in component code.

---

# 18. Design-to-Dev Handoff & Token Governance

- All tokens in Section 6 must be mirrored 1:1 in the Figma variables panel — same names, same values. No token exists in one place and not the other.
- Any new color/spacing value used in a component PR that isn't in this doc must be added here in the same PR — this file is the single source of truth, not tribal knowledge.
- Version this file (v1.0, v2.0...) and log changes in the Changelog section at the top, same pattern used in this revision.

---

# 19. UI Quality Assurance Sign-Off Checklist

- [ ] Conforms to color tokens and glassmorphism styling
- [ ] Trust Score renders with icon + shape + color (never color-only)
- [ ] Verified against colorblind simulator (deuteranopia/protanopia)
- [ ] Includes XAI evidence rationale with icon-paired severity
- [ ] Passes WCAG 2.1 AA contrast
- [ ] Responsive at all 6 breakpoints (320px to 1440px+)
- [ ] Skeleton loading + empty states implemented
- [ ] Keyboard focus rings + aria-labels present
- [ ] Respects `prefers-reduced-motion`
- [ ] Hindi/Devanagari rendering tested if `lang="hi"`
- [ ] New tokens (if any) added to this doc + Figma in the same PR

---
**[ END OF DESIGN SYSTEM SPECIFICATION v2.0 ]**
