import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Creates or updates default admin superuser credentials."

    def handle(self, *args, **options):
        User = get_user_model()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@printplanet.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "Admin@12345")
        first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "Admin")
        last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "User")

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": first_name,
                "last_name": last_name,
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            }
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()

        if created:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{email}' created successfully with configured password."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Superuser '{email}' password and permissions updated successfully."))
