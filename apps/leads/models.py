from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedUUIDModel

class ContactInquiry(TimeStampedUUIDModel):
    class Status(models.TextChoices):
        NEW = "new", "New"
        CONTACTED = "contacted", "Contacted"
        QUOTE_SENT = "quote_sent", "Quote Sent"
        CONVERTED = "converted", "Won / Converted"
        CLOSED = "closed", "Closed / Lost"

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.NEW)
    status_reason = models.TextField(blank=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="assigned_inquiries")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="updated_inquiries")

    class Meta:
        indexes = [models.Index(fields=["status", "created_at"])]

    def __str__(self):
        return f"{self.name} ({self.email})"

class LeadActivity(TimeStampedUUIDModel):
    inquiry = models.ForeignKey(ContactInquiry, on_delete=models.CASCADE, related_name="activities")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="lead_activities")
    note = models.TextField()

    def __str__(self):
        return f"Note by {self.author} on {self.inquiry.name}"
