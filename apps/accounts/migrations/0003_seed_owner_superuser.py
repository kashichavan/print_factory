from django.db import migrations
from django.contrib.auth.hashers import make_password

def seed_owner_superuser(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    if not User.objects.filter(is_superuser=True).exists():
        User.objects.create(
            email="printplanet16@gmail.com",
            first_name="Owner",
            last_name="Admin",
            password=make_password("admin12345"),
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )

def remove_owner_superuser(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_managers'),
    ]

    operations = [
        migrations.RunPython(seed_owner_superuser, remove_owner_superuser),
    ]
