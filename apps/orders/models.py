from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedUUIDModel
from apps.accounts.models import Address, Organization
from apps.catalog.models import Product, ProductVariant
from apps.quotes.models import QuoteRequest

class Cart(TimeStampedUUIDModel):
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name="carts")
    session_key = models.CharField(max_length=64, blank=True, db_index=True)
    is_active = models.BooleanField(default=True)

class CartItem(TimeStampedUUIDModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=1)
    specifications = models.JSONField(default=dict, blank=True)
    class Meta: constraints = [models.UniqueConstraint(fields=["cart", "product", "variant"], name="unique_cart_product_variant")]

class Order(TimeStampedUUIDModel):
    class Status(models.TextChoices): PENDING = "pending", "Pending"; CONFIRMED = "confirmed", "Confirmed"; IN_PRODUCTION = "production", "In production"; SHIPPED = "shipped", "Shipped"; DELIVERED = "delivered", "Delivered"; CANCELLED = "cancelled", "Cancelled"
    number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    customer_name = models.CharField(max_length=255, blank=True)
    customer_email = models.CharField(max_length=255, blank=True)
    customer_phone = models.CharField(max_length=50, blank=True)
    artwork_file = models.FileField(upload_to="order_artworks/", blank=True, null=True)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")
    quote_request = models.OneToOneField(QuoteRequest, on_delete=models.SET_NULL, null=True, blank=True, related_name="order")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    billing_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="billing_orders")
    shipping_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name="shipping_orders")
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    notes = models.TextField(blank=True)

    @property
    def total_amount(self):
        return self.subtotal + self.tax_amount + self.shipping_amount - self.discount_amount

    class Meta: indexes = [models.Index(fields=["status", "created_at"]), models.Index(fields=["customer", "created_at"])]

class OrderItem(TimeStampedUUIDModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, null=True, blank=True)
    product_name = models.CharField(max_length=255)
    sku = models.CharField(max_length=80, blank=True)
    quantity = models.PositiveIntegerField()
    specifications = models.JSONField(default=dict, blank=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    setup_charge = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))

    @property
    def total_price(self):
        return round(self.unit_price * self.quantity, 2)

class Payment(TimeStampedUUIDModel):
    class Status(models.TextChoices): PENDING = "pending", "Pending"; AUTHORIZED = "authorized", "Authorized"; PAID = "paid", "Paid"; FAILED = "failed", "Failed"; REFUNDED = "refunded", "Refunded"
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    provider = models.CharField(max_length=40)
    provider_payment_id = models.CharField(max_length=255, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    class Meta: indexes = [models.Index(fields=["provider", "provider_payment_id"])]

class Shipment(TimeStampedUUIDModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="shipments")
    carrier = models.CharField(max_length=100, blank=True)
    tracking_number = models.CharField(max_length=120, blank=True)
    shipped_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)
