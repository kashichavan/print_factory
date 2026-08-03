# Glassmorphism & Modern Lighting Effects

Glassmorphism provides tactile depth through semi-translucent surfaces, frosted background blurs, subtle border highlights, and ambient light reflections.

---

## 1. Glassmorphism CSS Recipe

```css
/* Premium Frosted Glass Card */
.glass-panel {
  background: rgba(255, 255, 255, 0.05); /* Dark mode tint */
  backdrop-filter: blur(16px) saturate(180%);
  -webkit-backdrop-filter: blur(16px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.125);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
  border-radius: 20px;
}

/* Light Theme Glass Variant */
.glass-panel-light {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(20px) saturate(160%);
  -webkit-backdrop-filter: blur(20px) saturate(160%);
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  border-radius: 20px;
}
```

---

## 2. Floating Navbar with Blur Effect

```css
.floating-nav {
  position: fixed;
  top: 20px;
  left: 50%;
  transform: translateX(-50%);
  width: calc(100% - 40px);
  max-width: 1100px;
  z-index: 1000;

  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  border-radius: 999px; /* Pill shape */

  background: rgba(18, 20, 29, 0.75);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}
```

---

## 3. Ambient Glow Orbs & Light Gradients

Create background lighting orbs to make glass surfaces shine:

```html
<div class="ambient-glow glow-1"></div>
<div class="ambient-glow glow-2"></div>
```

```css
.ambient-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
  z-index: 0;
  opacity: 0.45;
}

.glow-1 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, var(--accent-purple), transparent 70%);
  top: -100px;
  left: -100px;
}

.glow-2 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, var(--accent-cyan), transparent 70%);
  bottom: -150px;
  right: -150px;
}
```
