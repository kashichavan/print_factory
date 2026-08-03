---
name: backend-python-django
description: Comprehensive guidelines for building enterprise-grade Python/Django backends, REST APIs, dynamic database architectures, and secure web applications.
---

# Backend Python & Django Engineering Skill

This skill provides production best practices for architecting, building, and deploying robust Python/Django backend systems.

## Key Principles & Patterns

### 1. Model Architecture & Database Best Practices
- **UUID & Timestamps**: Inherit all domain models from explicit `TimeStampedUUIDModel` (with `id = UUIDField`, `created_at`, `updated_at`).
- **Publishable Models**: Use `is_active = BooleanField(default=True)` for non-destructive soft toggles.
- **Explicit Database Indexing**: Add `models.Index` on high-cardinality search fields like `[is_active, category]`, `[status, created_at]`.
- **Media File Safety**: Define `upload_to="catalog/%Y/%m/"` and create property methods like `@property get_image_url` to fallback gracefully between media, static assets, or placeholder images without throwing 404 or `ValueError` crashes.

### 2. Query Optimization (No N+1 Queries)
- **`select_related`**: Use for single-valued relationships (`ForeignKey`, `OneToOneField`).
- **`prefetch_related`**: Use for multi-valued relationships (`ManyToManyField`, reverse `ForeignKey`).
- **Paginator Enforcement**: Always wrap list endpoints in `django.core.paginator.Paginator(qs, per_page)` to prevent memory overruns.

### 3. Clean View Logic & Dynamic Options Parsing
- Separate business logic into helper methods or services.
- Parse dynamic options and volume price rules securely from request payloads.
- Use explicit `@login_required` and `@staff_required` decorators for administrative endpoints.

### 4. Admin Customization
- Register models with inline editors (`admin.TabularInline`) for quick bulk entry of child records (e.g. `ProductImage`, `ProductOption`, `PriceRule`).
