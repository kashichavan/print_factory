---
name: saas-architecture
description: Blueprint for designing multi-tenant B2B/B2C SaaS platforms, dynamic pricing engines, subscription billing workflows, staff attribution, and analytics control centers.
---

# SaaS Architecture Skill Package

This skill establishes standard patterns for constructing scalable, multi-tenant SaaS products and e-commerce platforms.

## Core SaaS Pillars

### 1. Multi-Tenant Organization & Staff Attribution
- **Organization Isolation**: Model domain entities with an optional `organization = ForeignKey(Organization)` for tenant scoping.
- **Staff Attribution Tracking**: Record `updated_by = ForeignKey(User)` and maintain activity history logs (`LeadActivity`) for accountability across team members.
- **Role-Based Access Control (RBAC)**: Distinguish between customer accounts, organization members, and internal staff admins (`is_staff`).

### 2. Dynamic Option & Tier-Based Pricing Engine
- **Base Price + Option Modifiers**: Calculate prices dynamically using `BasePrice * TierMultiplier + Sum(SelectedOptionModifiers)`.
- **Quantity Volume Discounts**: Define quantity tiers (`PriceRule.minimum_quantity`) with instant savings badges (`Save 20%`, `Best Value`).

### 3. Operational Pipeline & Status Tracking
- **Order & Job Workflows**: Pipeline order statuses (`Pending` -> `Confirmed` -> `In Production` -> `Shipped` -> `Delivered`).
- **Carrier Tracking Integration**: Store courier names and AWB tracking numbers for real-time customer updates.
- **Customer Feedback & Proof Approval**: Store customer proofing decisions and review ratings alongside production jobs.
