from decimal import Decimal
from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedUUIDModel
from apps.accounts.models import Organization
from apps.catalog.models import Product

class QuoteRequest(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"; SUBMITTED = "submitted", "Submitted"; REVIEWING = "reviewing", "Reviewing"; QUOTED = "quoted", "Quoted"; ACCEPTED = "accepted", "Accepted"; DECLINED = "declined", "Declined"; EXPIRED = "expired", "Expired"
    number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="quote_requests")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name="quote_requests")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    contact_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True)
    required_by = models.DateField(blank=True, null=True)
    class Meta: indexes = [models.Index(fields=["status", "created_at"]), models.Index(fields=["customer", "created_at"])]

class QuoteLine(TimeStampedUUIDModel):
    quote_request = models.ForeignKey(QuoteRequest, on_delete=models.CASCADE, related_name="lines")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="quote_lines")
    quantity = models.PositiveIntegerField()
    specifications = models.JSONField(default=dict, blank=True)
    description = models.TextField(blank=True)

class ArtworkFile(TimeStampedUUIDModel):
    class ReviewStatus(models.TextChoices): PENDING = "pending", "Pending"; APPROVED = "approved", "Approved"; CHANGES = "changes", "Changes requested"
    quote_line = models.ForeignKey(QuoteLine, on_delete=models.CASCADE, related_name="artwork_files")
    file = models.FileField(upload_to="artwork/%Y/%m/")
    original_filename = models.CharField(max_length=255)
    review_status = models.CharField(max_length=16, choices=ReviewStatus.choices, default=ReviewStatus.PENDING)
    review_notes = models.TextField(blank=True)

class Quote(TimeStampedUUIDModel):
    quote_request = models.ForeignKey(QuoteRequest, on_delete=models.CASCADE, related_name="revisions")
    revision = models.PositiveSmallIntegerField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    valid_until = models.DateField(blank=True, null=True)
    terms = models.TextField(blank=True)
    class Meta: constraints = [models.UniqueConstraint(fields=["quote_request", "revision"], name="unique_quote_revision")]

class QuoteLinePrice(TimeStampedUUIDModel):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE, related_name="line_prices")
    quote_line = models.ForeignKey(QuoteLine, on_delete=models.PROTECT, related_name="prices")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    setup_charge = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))
