# TruthShield X — Frontend Folder Structure Guide

The `apps/web/src` directory is organized into strict functional modules:

```
apps/web/src/
  ├── app/          # Global application providers & app context
  ├── assets/       # Static images, icons, and logos
  ├── components/   # UI Component Library
  │   ├── common/   # Reusable domain widgets (TrustScoreGauge, SectionHeader, TooltipDisabled)
  │   ├── layout/   # Layout elements (Header, Sidebar, Footer, Breadcrumbs, NotificationsDrawer)
  │   └── ui/       # Atom components (Button, Input, Card, Modal, Badge, UploadZone, etc.)
  ├── features/     # Feature-specific schemas & validation logic (auth/, etc.)
  ├── hooks/        # Custom React hooks (useTheme, useSidebar, usei18n, useReducedMotion)
  ├── i18n/         # Internationalization config (i18n.ts, locales/en.json, locales/hi.json)
  ├── layouts/      # Page layout templates (AuthLayout, DashboardLayout, FullWidthLayout, AdminLayout)
  ├── lib/          # Utilities & libraries (sonner.ts, motion.ts, cn.ts)
  ├── pages/        # Route page entry points (LoginPage, DashboardPage, ProfilePage, etc.)
  ├── router/       # Router setup, ProtectedRoute guard, and ErrorBoundary wrappers
  ├── services/     # API services & mock data generators matching Phase 1 envelope
  ├── store/        # Zustand state stores (useAuthStore, useThemeStore, useSidebarStore, etc.)
  ├── styles/       # HSL variables, glassmorphic CSS rules, and reduced motion utilities
  ├── types/        # TypeScript interfaces & API envelope definitions
  └── utils/        # Utility helpers (score.ts, cn.ts, date formatting)
```
