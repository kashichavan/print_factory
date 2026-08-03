# Micro-animations & CSS Keyframes

Micro-interactions guide user attention, provide physical feedback, and make web interfaces feel interactive and refined.

---

## 1. Shimmering Border Animation

```css
@keyframes border-shimmer {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.shimmer-button {
  position: relative;
  padding: 14px 28px;
  border-radius: 99px;
  background: linear-gradient(90deg, #13151c, #2a2e3d, #13151c);
  background-size: 200% 200%;
  animation: border-shimmer 4s ease infinite;
  color: #fff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  cursor: pointer;
  overflow: hidden;
  transition: transform 200ms ease, box-shadow 200ms ease;
}

.shimmer-button:hover {
  transform: scale(1.03);
  box-shadow: 0 0 25px rgba(255, 255, 255, 0.25);
}
```

---

## 2. Floating Ambient Motion

```css
@keyframes float-subtle {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-10px) rotate(1deg); }
}

.floating-element {
  animation: float-subtle 6s ease-in-out infinite;
}
```

---

## 3. Pulse Aura / Online Badge

```css
@keyframes pulse-ring {
  0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(22, 219, 137, 0.7); }
  70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(22, 219, 137, 0); }
  100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(22, 219, 137, 0); }
}

.status-badge-online {
  width: 10px;
  height: 10px;
  background: #16db89;
  border-radius: 50%;
  animation: pulse-ring 2s infinite;
}
```

---

## 4. Smooth Staggered Entrance Reveal

```css
@keyframes fade-slide-up {
  from {
    opacity: 0;
    transform: translateY(24px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-entrance {
  animation: fade-slide-up 600ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

.delay-1 { animation-delay: 100ms; }
.delay-2 { animation-delay: 200ms; }
.delay-3 { animation-delay: 300ms; }
```
