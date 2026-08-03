from django.test import TestCase
from django.urls import reverse
from apps.accounts.models import Address, User
from apps.catalog.models import Category, Product
from apps.orders.models import Order
from apps.production.models import ProductionJob


class OwnerDashboardTests(TestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(email="owner@example.com", password="pass12345")
        self.category = Category.objects.create(name="Cards", slug="cards")
        self.customer = User.objects.create_user(email="customer@example.com", password="pass12345")
        self.address = Address.objects.create(user=self.customer, recipient_name="Customer", phone="9000000000", line1="1 Main Road", city="Pune", state="Maharashtra", postal_code="411001")

    def test_dashboard_is_staff_only(self):
        response = self.client.get(reverse("dashboard:home"))
        self.assertRedirects(response, "/owner/login/?next=/owner/")
        self.client.force_login(self.customer)
        response = self.client.get(reverse("dashboard:home"))
        self.assertEqual(response.status_code, 302)

    def test_owner_can_create_product(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("dashboard:product_create"), {"name": "Premium brochure", "category": self.category.id, "product_type": "print", "short_description": "A crisp brochure", "description": "", "requires_quote": "on", "is_active": "on"})
        self.assertRedirects(response, reverse("dashboard:product_list"))
        self.assertEqual(Product.objects.get().slug, "premium-brochure")

    def test_order_status_creates_production_job_and_tracking(self):
        order = Order.objects.create(number="ORD-2001", customer=self.customer, billing_address=self.address, shipping_address=self.address)
        self.client.force_login(self.owner)
        response = self.client.post(reverse("dashboard:order_detail", args=[order.id]), {"status": "production", "notes": "Print run started", "carrier": "", "tracking_number": ""})
        self.assertRedirects(response, reverse("dashboard:order_detail", args=[order.id]))
        self.assertTrue(ProductionJob.objects.filter(order=order).exists())
        response = self.client.post(reverse("dashboard:order_detail", args=[order.id]), {"status": "shipped", "notes": "", "carrier": "Delhivery", "tracking_number": "TRACK-2001"})
        order.refresh_from_db()
        self.assertEqual(order.shipments.get().tracking_number, "TRACK-2001")
