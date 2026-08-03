from django.test import TestCase
from django.urls import reverse
from apps.leads.models import ContactInquiry


class PublicPagesTests(TestCase):
    def test_home_page_renders(self):
        response = self.client.get(reverse("content:home"))
        self.assertContains(response, "Make your")

    def test_contact_form_creates_sales_inquiry(self):
        response = self.client.post(reverse("content:contact"), {"name": "Priya", "email": "priya@example.com", "phone": "9000000000", "message": "Need 500 catalogues"})
        self.assertRedirects(response, reverse("content:contact"))
        self.assertEqual(ContactInquiry.objects.get().name, "Priya")
