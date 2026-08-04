# TruthShield X — i18n & Multilingual Guide

## Overview
TruthShield X uses `i18next` and `react-i18next` for internationalization. All user-facing strings are stored in JSON locale key files.

## Files
- `src/i18n/locales/en.json`: English translation key catalog.
- `src/i18n/locales/hi.json`: Hindi Devanagari translation key catalog.

## Adding a New Translation Key
1. Open `src/i18n/locales/en.json` and add the key under the appropriate section:
   ```json
   {
     "dashboard": {
       "newKey": "New Feature Heading"
     }
   }
   ```
2. Open `src/i18n/locales/hi.json` and add the corresponding Devanagari translation:
   ```json
   {
     "dashboard": {
       "newKey": "नई सुविधा शीर्षक"
     }
   }
   ```
3. Consume in components using `usei18n` hook or `t` function:
   ```tsx
   import { usei18n } from '@/hooks/usei18n';

   const { t } = usei18n();
   return <h1>{t('dashboard.newKey')}</h1>;
   ```

## Devanagari Font Behavior
When language is set to `hi`, `document.body` receives the `font-devanagari` CSS class, loading `Noto Sans Devanagari` and increasing line-height by 10% (`1.5` -> `1.65`) for optimal vertical breathing room.
