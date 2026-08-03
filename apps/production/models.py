from django.conf import settings
from django.db import models
from apps.core.models import TimeStampedUUIDModel
from apps.orders.models import Order

class ProductionJob(TimeStampedUUIDModel):
    class Status(models.TextChoices): QUEUED = "queued", "Queued"; IN_PROGRESS = "in_progress", "In progress"; QUALITY_CHECK = "quality_check", "Quality check"; COMPLETE = "complete", "Complete"
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="production_jobs")
    job_number = models.CharField(max_length=30, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)
    due_at = models.DateTimeField(blank=True, null=True)
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, related_name="production_jobs")
    class Meta: indexes = [models.Index(fields=["status", "due_at"])]

class ProductionTask(TimeStampedUUIDModel):
    job = models.ForeignKey(ProductionJob, on_delete=models.CASCADE, related_name="tasks")
    name = models.CharField(max_length=255)
    is_complete = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField(default=0)
    class Meta: ordering = ["position"]
