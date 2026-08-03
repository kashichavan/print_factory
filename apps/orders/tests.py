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
