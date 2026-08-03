# Print Planet

Scalable Django + Django REST Framework foundation for a printing and corporate-gifting business. The UI will use Django templates with HTML/CSS, while the API remains available for customer portal and future mobile integrations.

## App boundaries

| App | Owns |
| --- | --- |
| `core` | UUIDs and audit timestamps shared by business models |
| `accounts` | Customer accounts, B2B organisations, memberships and addresses |
| `catalog` | Categories, products, images, options, variants and quantity pricing |
| `quotes` | Custom print requests, artwork uploads, quote revisions and pricing |
| `orders` | Carts, immutable order snapshots, payments and shipments |
| `content` | Services, partner logos and FAQs displayed on the website |
| `leads` | Contact-form enquiries and sales follow-up |
| `production` | Internal production jobs and tasks after an order is confirmed |

## Customer journey

`Browse product → choose print options / upload artwork → request quote or buy → pay → production → dispatch → delivery`

The customer portal will expose profile, addresses, company details, quote/artwork approval status, order history, payments, tracking, and reordering. A customer can belong to a company, allowing B2B buyers to keep shared billing and delivery data without sharing a login.

## Local setup

```bash
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

SQLite is used only for local development. Configure the `DB_*` variables from `.env.example` for PostgreSQL in any shared environment. The custom `accounts.User` model is already in the first migration; do not replace it later.

## Implementation order

1. Build customer registration/login and the public catalogue HTML pages.
2. Add DRF serializers and endpoints for catalogue, quote submission, cart and customer portal.
3. Add payment provider, email/SMS notifications and cloud object storage for artwork.
4. Add staff dashboard and production workflow.
