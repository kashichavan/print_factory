# Design Tokens & Color Palettes (Trending UI 2026)

This reference outlines modern CSS custom properties, color systems, typography scale, elevation levels, and lighting tokens.

---

## 1. Curated Color Palettes

### A. Dark Velvet & Neon Aura (Cyber / Tech)
```css
:root {
  /* Core Base Colors */
  --bg-dark: hsl(240, 25%, 7%);
  --bg-surface-1: hsl(240, 20%, 11%);
  --bg-surface-2: hsl(240, 18%, 16%);
  --bg-surface-glass: hsla(240, 20%, 15%, 0.55);
  
  /* Text & Foreground */
  --text-primary: hsl(0, 0%, 98%);
  --text-secondary: hsl(240, 10%, 70%);
  --text-muted: hsl(240, 8%, 50%);

  /* Neon Accents */
  --accent-cyan: hsl(186, 100%, 50%);
  --accent-purple: hsl(272, 90%, 65%);
  --accent-emerald: hsl(158, 85%, 52%);
  --accent-orange: hsl(18, 100%, 62%);

  /* Borders & Glows */
  --border-subtle: hsla(240, 15%, 85%, 0.12);
  --border-active: hsla(186, 100%, 50%, 0.4);
  --glow-cyan: 0 0 25px hsla(186, 100%, 50%, 0.35);
  --glow-purple: 0 0 30px hsla(272, 90%, 65%, 0.3);
}
```

### B. Warm Paper & Premium Ink (Luxury Editorial / Studio)
```css
:root {
  --bg-paper: #f9f6f0;
  --bg-card: #ffffff;
  --bg-subtle: #eee9df;
  
  --ink-main: #13151c;
  --ink-body: #424656;
  --ink-muted: #787d90;

  --accent-coral: #ff5738;
  --accent-lime: #d4f04d;
  --accent-lavender: #c2b5fc;

  --shadow-sm: 0 2px 8px rgba(19, 21, 28, 0.04);
  --shadow-md: 0 10px 30px rgba(19, 21, 28, 0.08);
  --shadow-lg: 0 24px 60px rgba(19, 21, 28, 0.12);
  --shadow-hard: 6px 6px 0px #13151c;
}
```

---

## 2. Fluid Typography Scale

Use `clamp()` for smooth responsiveness across mobile, tablet, and ultra-wide desktops.

```css
:root {
  --font-main: 'Plus Jakarta Sans', 'Inter', -apple-system, sans-serif;
  --font-heading: 'Fraunces', 'Outfit', Georgia, serif;
  --font-mono: 'JetBrains Mono', monospace;

  /* Typography Scale */
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.83rem + 0.25vw, 1rem);
  --text-base: clamp(1rem, 0.95rem + 0.3vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1.05rem + 0.4vw, 1.25rem);
  --text-xl: clamp(1.35rem, 1.2rem + 0.7vw, 1.75rem);
  --text-2xl: clamp(1.8rem, 1.5rem + 1.2vw, 2.5rem);
  --text-3xl: clamp(2.4rem, 1.9rem + 2.2vw, 3.75rem);
  --text-hero: clamp(3.2rem, 2.5rem + 4vw, 5.5rem);
}
```

---

## 3. Spring Transitions & Curves

```css
:root {
  --ease-spring: cubic-bezier(0.175, 0.885, 0.32, 1.275);
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
  --ease-in-out-smooth: cubic-bezier(0.4, 0, 0.2, 1);

  --transition-fast: 150ms var(--ease-out-expo);
  --transition-normal: 300ms var(--ease-out-expo);
  --transition-slow: 500ms var(--ease-out-expo);
}
```
