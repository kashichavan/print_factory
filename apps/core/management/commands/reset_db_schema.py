from django.core.management.base import BaseCommand
from django.db import connection, transaction

class Command(BaseCommand):
    help = "Drops all existing tables in public schema to allow a fresh deployment/migration."

    def handle(self, *args, **options):
        self.stdout.write("Dropping all existing database tables...")
        with connection.cursor() as cursor:
            cursor.execute("DROP SCHEMA public CASCADE;")
            cursor.execute("CREATE SCHEMA public;")
            cursor.execute("GRANT ALL ON SCHEMA public TO public;")
        self.stdout.write(self.style.SUCCESS("Database schema reset successfully! Ready for fresh migration."))
