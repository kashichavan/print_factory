from django.test import TestCase
from apps.accounts.models import Address, User
from apps.catalog.models import Category, Product, ProductVariant
from .models import Order, OrderItem, Payment, Shipment


class OrderModelTests(TestCase):
    def test_order_preserves_product_snapshot_and_fulfilment_records(self):
        user = User.objects.create_user(email="order@example.com", password="pass12345")
        address = Address.objects.create(user=user, recipient_name="Order Customer", phone="9000000000", line1="42 Print Street", city="Mumbai", state="Maharashtra", postal_code="400001")
        category = Category.objects.create(name="Gifts", slug="gifts")
        product = Product.objects.create(name="Branded mug", slug="branded-mug", category=category, product_type="gift")
        variant = ProductVariant.objects.create(product=product, sku="MUG-WHITE", price="499.00")
        order = Order.objects.create(number="ORD-1001", customer=user, billing_address=address, shipping_address=address, subtotal="998.00")
        item = OrderItem.objects.create(order=order, product=product, variant=variant, product_name="Branded mug", sku="MUG-WHITE", quantity=2, unit_price="499.00")
        payment = Payment.objects.create(order=order, provider="razorpay", amount="998.00", status="paid")
        shipment = Shipment.objects.create(order=order, carrier="Delhivery", tracking_number="TRACK-123")
        self.assertEqual(order.items.get(), item)
        self.assertEqual(payment.order, order)
        self.assertEqual(shipment.order, order)

    def test_checkout_collects_user_info_and_creates_order_for_owner(self):
        category, _ = Category.objects.get_or_create(slug="business-cards-test", defaults={"name": "Business Cards Test"})
        product, _ = Product.objects.get_or_create(slug="standard-card-test", defaults={"name": "Standard Card Test", "category": category, "base_price": "190.00"})
        
        # Add to cart
        self.client.post("/cart/add/", data={"product_id": str(product.id), "quantity": 100, "total_price": "190.00"}, content_type="application/json")
        
        # Perform checkout
        response = self.client.post("/cart/checkout/", data={
            "customer_name": "Test Owner Order",
            "customer_email": "ownerorder@example.com",
            "customer_phone": "+91 9876543210",
            "notes": "Express delivery requested"
        })

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        
        order = Order.objects.get(number=data["order_number"])
        self.assertEqual(order.customer_name, "Test Owner Order")
        self.assertEqual(order.customer_email, "ownerorder@example.com")
        self.assertEqual(order.customer_phone, "+91 9876543210")
        self.assertEqual(order.items.count(), 1)

