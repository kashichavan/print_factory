from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import Address, User
from apps.catalog.models import Category, Product, ProductOption, PriceRule
from apps.leads.models import ContactInquiry, LeadActivity
from apps.orders.models import Order
from apps.production.models import ProductionJob


class OwnerDashboardTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(email="owner@example.com", password="pass12345")
        self.category = Category.objects.create(name="Cards", slug="cards")
        self.customer = User.objects.create_user(email="customer@example.com", password="pass12345")
        self.address = Address.objects.create(
            user=self.customer,
            recipient_name="Customer",
            phone="9000000000",
            line1="1 Main Road",
            city="Pune",
            state="Maharashtra",
            postal_code="411001"
        )

    def test_dashboard_is_staff_only(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertRedirects(response, "/owner/login/?next=/owner/")
        self.client.force_login(self.customer)
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 302)

    def test_owner_can_create_product_with_dynamic_options_and_tiers(self):
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("dashboard:product_create"),
            {
                "name": "Premium brochure",
                "category": self.category.id,
                "product_type": "print",
                "base_price": "250.00",
                "short_description": "A crisp brochure",
                "description": "Full spec details",
                "requires_quote": "on",
                "is_active": "on",
                "dyn_option_name[]": ["Paper Stock"],
                "dyn_option_values[]": ["Standard 300gsm:0, Glossy 350gsm:50"],
                "tier_min_qty[]": ["100", "500"],
                "tier_unit_price[]": ["250.00", "1000.00"],
            }
        )
        self.assertRedirects(response, reverse("dashboard:product_list"))
        prod = Product.objects.get(name="Premium brochure")
        self.assertEqual(prod.slug, "premium-brochure")
        self.assertTrue(prod.options.filter(name="Paper Stock").exists())
        self.assertEqual(prod.price_rules.count(), 2)

    def test_owner_can_toggle_and_edit_product(self):
        self.client.force_login(self.owner)
        prod = Product.objects.create(name="Flyers", slug="flyers", category=self.category, base_price=Decimal("150.00"))
        
        # Toggle status
        response = self.client.get(reverse("dashboard:product_toggle", args=[prod.pk]))
        self.assertRedirects(response, reverse("dashboard:product_list"))
        prod.refresh_from_db()
        self.assertFalse(prod.is_active)

        # Edit product
        response = self.client.post(
            reverse("dashboard:product_edit", args=[prod.pk]),
            {
                "name": "Ultra Glossy Flyers",
                "category": self.category.id,
                "product_type": "print",
                "base_price": "180.00",
                "is_active": "on",
            }
        )
        self.assertRedirects(response, reverse("dashboard:product_list"))
        prod.refresh_from_db()
        self.assertEqual(prod.name, "Ultra Glossy Flyers")
        self.assertEqual(prod.base_price, Decimal("180.00"))

    def test_order_status_creates_production_job_and_tracking(self):
        order = Order.objects.create(number="ORD-2001", customer=self.customer, billing_address=self.address, shipping_address=self.address)
        self.client.force_login(self.owner)
        response = self.client.post(
            reverse("dashboard:order_detail", args=[order.id]),
            {"status": "production", "notes": "Print run started", "carrier": "", "tracking_number": ""}
        )
        self.assertRedirects(response, reverse("dashboard:order_detail", args=[order.id]))
        self.assertTrue(ProductionJob.objects.filter(order=order).exists())
        
        response = self.client.post(
            reverse("dashboard:order_detail", args=[order.id]),
            {"status": "shipped", "notes": "", "carrier": "Delhivery", "tracking_number": "TRACK-2001"}
        )
        order.refresh_from_db()
        self.assertEqual(order.shipments.get().tracking_number, "TRACK-2001")

    def test_lead_update_with_staff_attribution(self):
        lead = ContactInquiry.objects.create(name="Rohit", email="rohit@example.com", phone="9876543210", message="500 Catalogues quote")
        self.client.force_login(self.owner)
        
        response = self.client.post(
            reverse("dashboard:lead_update", args=[lead.pk]),
            {"status": "in_progress", "status_reason": "Quotation sent via email", "note": "Follow up on Thursday"}
        )
        self.assertRedirects(response, reverse("dashboard:lead_list"))
        lead.refresh_from_db()
        self.assertEqual(lead.status, "in_progress")
        self.assertEqual(lead.updated_by, self.owner)
        self.assertTrue(LeadActivity.objects.filter(inquiry=lead).exists())
