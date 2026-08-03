from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedUUIDModel

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if not extra_fields.get("is_staff") or not extra_fields.get("is_superuser"):
            raise ValueError("Superusers must have is_staff=True and is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
    class Meta:
        ordering = ["-date_joined"]

class Organization(TimeStampedUUIDModel):
    name = models.CharField(max_length=255)
    gstin = models.CharField(max_length=15, blank=True)
    billing_email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    class Meta:
        indexes = [models.Index(fields=["name"])]

class OrganizationMember(TimeStampedUUIDModel):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="organization_memberships")
    role = models.CharField(max_length=20, choices=[("owner", "Owner"), ("buyer", "Buyer"), ("viewer", "Viewer")], default="buyer")
    class Meta:
        constraints = [models.UniqueConstraint(fields=["organization", "user"], name="unique_organization_member")]

class Address(TimeStampedUUIDModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, blank=True, null=True, related_name="addresses")
    label = models.CharField(max_length=50, default="Home")
    recipient_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    line1 = models.CharField(max_length=255)
    line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=12)
    country = models.CharField(max_length=2, default="IN")
    is_default = models.BooleanField(default=False)
