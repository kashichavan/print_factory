---
name: dynamic-ui-components
description: Antigravity skill for building interactive, state-driven UI components with smooth micro-animations, drawers, toasts, live filters, and dynamic calculators.
---

# Dynamic UI Components & Micro-Interactions Skill

This skill provides patterns and design specifications for building highly dynamic, responsive, stateful UI components.

---

## 1. Dynamic Live Search & Real-Time Filtering
Implement instant client-side filtering without full page reloads:
```javascript
function initLiveSearch(inputId, cardSelector) {
  const input = document.getElementById(inputId);
  if (!input) return;
  input.addEventListener('input', (e) => {
    const q = e.target.value.toLowerCase().trim();
    document.querySelectorAll(cardSelector).forEach(card => {
      const text = card.textContent.toLowerCase();
      card.style.display = text.includes(q) ? '' : 'none';
    });
  });
}
```

---

## 2. Interactive Calculator Engine
```javascript
function calculateDynamicPrice(base, mult, extras = []) {
  const extraSum = extras.reduce((a, b) => a + b, 0);
  return (base * mult) + extraSum;
}
```

---

## 3. Toast Notifications & Floating Widgets
Provide immediate feedback on user actions (e.g., item added to cart, copy to clipboard, order updated).
