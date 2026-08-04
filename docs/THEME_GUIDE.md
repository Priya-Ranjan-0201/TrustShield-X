# TruthShield X — Theme Engine & Anti-Flash Guide

## Persistence
Theme state (`dark` | `light` | `system`) is persisted in `localStorage` under the key `tsx-theme`.

## Anti-Flash Pre-Paint Resolution
To prevent flash-of-wrong-theme on page load, an inline synchronous JavaScript snippet in `index.html` inspects `tsx-theme` and `window.matchMedia('(prefers-color-scheme: dark)')` before the initial DOM render:

```html
<script>
  (function() {
    try {
      var theme = localStorage.getItem('tsx-theme') || 'system';
      var resolved = theme;
      if (theme === 'system') {
        resolved = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      if (resolved === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.add('light');
      }
    } catch (e) {}
  })();
</script>
```

## System Theme Resolver
Changes to the operating system's color scheme are dynamically re-evaluated via media query event listeners when `theme === 'system'`.
