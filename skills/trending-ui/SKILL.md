---
name: trending-ui
description: Professional skill for building ultra-modern, trending UI/UX web applications in Google Antigravity. Covers Bento grids, glassmorphism, OKLCH/HSL color palettes, dynamic micro-animations, floating navbars, dark mode, and responsive layout patterns.
---

# Trending UI/UX Design Skill for Antigravity

This skill equips Antigravity with guidelines, design tokens, micro-animations, and component blueprints to create visually stunning, premium 2026-era web applications.

---

## Core Design Principles

1. **Visual Excellence & High Contrast**
   - Never rely on plain default colors (`#ff0000`, `blue`, `#333`). Use curated HSL / OKLCH color palettes with depth, vibrant accents, and smooth contrast ratios.
   - Default to rich dark or warm paper light themes with subtle mesh gradients.

2. **Bento Grid Layouts**
   - Use dynamic multi-size card grids (`grid-column: span X`, `grid-row: span Y`) to highlight key features, stats, media, and interactive controls with visual hierarchy.

3. **Glassmorphism & Layering**
   - Utilize `backdrop-filter: blur(16px)`, translucent background alpha fills (`hsla(...)` or `rgba(255, 255, 255, 0.08)`), and subtle 1px border highlights (`border: 1px solid rgba(255, 255, 255, 0.12)`).

4. **Micro-interactions & Keyframe Animations**
   - Apply hover translations (`transform: translateY(-4px)`), smooth spring transitions (`cubic-bezier(0.16, 1, 0.3, 1)`), glowing borders, ambient aura effects, and interactive magnetic button states.

5. **Fluid Modern Typography**
   - Use modern Variable Fonts (`Inter`, `Plus Jakarta Sans`, `Outfit`, `Fraunces`, `Space Grotesk`).
   - Implement fluid text sizes with CSS `clamp(min, preferred, max)` and tight heading letter-spacing (`-0.03em` to `-0.05em`).

---

## Detailed References

When building or updating UI components, inspect the detailed references in `references/`:

- [Design Tokens & Color Palettes](file:///skills/trending-ui/references/design-tokens.md) — OKLCH & HSL color tokens, typography scales, glass variables, gradient definitions.
- [Bento Grid Specifications](file:///skills/trending-ui/references/bento-grid.md) — Responsive multi-span card patterns, feature highlights, and dashboard widgets.
- [Glassmorphism & Lighting](file:///skills/trending-ui/references/glassmorphism.md) — Backdrop blurs, light reflections, ambient glows, frosted card layers.
- [Micro-animations & Keyframes](file:///skills/trending-ui/references/micro-animations.md) — Hover transitions, border shimmers, pulse glows, floating elements.
- [Component Blueprints](file:///skills/trending-ui/references/component-library.md) — Ready-to-use HTML/CSS patterns for navbars, hero sections, product cards, pricing, and forms.

---

## Quick Workflow Checklist for UI Tasks

When implementing a UI feature:
1. **Define Design Tokens**: Set up primary, secondary, surface, border, and glow variables in `:root`.
2. **Setup Glass & Depth**: Add subtle drop shadows, backdrop filters, and semi-transparent backgrounds.
3. **Structure Grid Layout**: Use Flexbox for alignments and CSS Grid / Bento patterns for content density.
4. **Add Micro-interactions**: Add hover states, active states, cursor feedback, and fluid cubic-bezier transitions.
5. **Ensure Responsiveness & Accessibility**: Verify mobile breakpoints (<768px), ARIA labels, focus states, and high contrast visibility.
