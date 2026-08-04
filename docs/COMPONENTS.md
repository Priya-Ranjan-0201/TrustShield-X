# TruthShield X — Component Library Guide

## Overview
All UI components in `apps/web/src/components` strictly consume HSL design tokens from `Design.md` via Tailwind CSS config. No hardcoded inline hex values are used outside designated brand tokens.

---

## 1. TrustScoreGauge
Radial SVG gauge displaying Digital Trust Score (0–100) with colorblind-safe shape + icon + label mapping (`Design.md` Section 9.2).

### Props
- `score` (`number`): Score value (0-100).
- `status` (`string`): Status tier text (e.g., `TRUSTED`, `DANGEROUS`).
- `size` (`'sm' | 'md' | 'lg'`): Size variant (default: `'md'`).

### Usage
```tsx
import { TrustScoreGauge } from '@/components/common/TrustScoreGauge';

<TrustScoreGauge score={94} status="TRUSTED" size="md" />
```

---

## 2. TooltipDisabled
Hover tooltip wrapper for disabled placeholder features per Phase 2 explicit decision table.

### Props
- `children` (`ReactNode`): Disabled button or element.
- `tooltipText` (`string`): Explanation message shown on hover.

### Usage
```tsx
import { TooltipDisabled } from '@/components/common/TooltipDisabled';

<TooltipDisabled tooltipText="Threat Intelligence module ships in Phase 17.">
  <button disabled className="opacity-50 cursor-not-allowed">Threat Intel</button>
</TooltipDisabled>
```

---

## 3. Button
Primary CTA and secondary action buttons supporting loading state spinner and icon adornments.

### Props
- `variant` (`'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive'`)
- `size` (`'sm' | 'md' | 'lg'`)
- `isLoading` (`boolean`): Displays spinning SVG icon and locks width.

---

## 4. Input
Text input component with error state (`AlertCircle` icon + red ring) and success state (`CheckCircle` icon + green ring).

---

## 5. UploadZone
Drag & drop file upload box featuring simulated progress bar state (`ProgressBar` component).
