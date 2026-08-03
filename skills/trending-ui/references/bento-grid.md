# Bento Grid Specifications & Layout Patterns

Bento grid layouts organize information into clean, unequal, modular cards—resembling a Japanese bento box.

---

## 1. Core Bento Grid CSS Architecture

```css
.bento-grid {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

/* Card Column Spans */
.bento-col-12 { grid-column: span 12; }
.bento-col-8  { grid-column: span 8; }
.bento-col-7  { grid-column: span 7; }
.bento-col-6  { grid-column: span 6; }
.bento-col-5  { grid-column: span 5; }
.bento-col-4  { grid-column: span 4; }
.bento-col-3  { grid-column: span 3; }

/* Mobile Fallback */
@media (max-width: 900px) {
  .bento-grid {
    grid-template-columns: repeat(6, 1fr);
  }
  .bento-col-8, .bento-col-7, .bento-col-5, .bento-col-4 {
    grid-column: span 6;
  }
}

@media (max-width: 600px) {
  .bento-grid {
    grid-template-columns: 1fr;
  }
  [class*="bento-col-"] {
    grid-column: span 1 !important;
  }
}
```

---

## 2. Bento Card Styling Rules

Every bento card should feature:
- Rounded corners (`border-radius: 24px` or `1.5rem`).
- Subtle background gradient or glass translucent fill.
- Inner padding (`padding: 28px` to `40px`).
- Subtle hover elevation and glowing border animation.

```css
.bento-card {
  position: relative;
  border-radius: 24px;
  background: var(--bg-surface-glass);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--border-subtle);
  padding: 32px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: transform 300ms var(--ease-out-expo),
              border-color 300ms var(--ease-out-expo),
              box-shadow 300ms var(--ease-out-expo);
}

.bento-card:hover {
  transform: translateY(-5px);
  border-color: var(--border-active);
  box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5), var(--glow-cyan);
}
```

---

## 3. High-Impact Bento Card Variants

1. **Hero Feature Card (span 8)**: Large title, product preview image/animation, call-to-action button, background mesh light.
2. **Metric / Stat Card (span 4)**: Large animated stat counter (e.g. `99.9%`), trend sparkline SVG, sub-label.
3. **Interactive Toggle Card (span 4)**: Live UI control switch, status pill indicator, instant state changes.
4. **Testimonial / Social Proof (span 4 or 6)**: Avatar stack, rating stars, glowing quotes.
