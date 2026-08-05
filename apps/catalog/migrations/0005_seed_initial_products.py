from django.db import migrations

def noop_seed(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_product_catalog_pro_is_acti_1a8de5_idx_and_more'),
    ]

    operations = [
        migrations.RunPython(noop_seed, noop_seed),
    ]
