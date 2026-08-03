from django.test import TestCase
from apps.accounts.models import User
from apps.catalog.models import Category, Product
from .models import Quote, QuoteLine, QuoteLinePrice, QuoteRequest


class QuoteModelTests(TestCase):
    def test_quote_revisions_and_line_price_are_linked_to_customer_request(self):
        user = User.objects.create_user(email="customer@example.com", password="pass12345")
        category = Category.objects.create(name="Cards", slug="cards")
        product = Product.objects.create(name="Wedding card", slug="wedding-card", category=category, product_type="print")
        request = QuoteRequest.objects.create(number="QR-1001", customer=user, contact_name="Customer", contact_email=user.email, contact_phone="9000000000", status="submitted")
        line = QuoteLine.objects.create(quote_request=request, product=product, quantity=200, specifications={"paper": "300 GSM"})
        quote = Quote.objects.create(quote_request=request, revision=1, subtotal="4000.00")
        price = QuoteLinePrice.objects.create(quote=quote, quote_line=line, unit_price="20.00", tax_rate="18.00")
        self.assertEqual(request.lines.get(), line)
        self.assertEqual(request.revisions.get(), quote)
        self.assertEqual(price.quote_line.specifications["paper"], "300 GSM")
