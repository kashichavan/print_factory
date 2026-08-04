from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from .models import Category, OptionValue, PriceRule, Product, ProductOption, ProductVariant


class CatalogModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Business Stationery", slug="business-stationery")
        self.product = Product.objects.create(
            name="Business Cards",
            slug="business-cards",
            category=self.category,
            product_type="print",
            base_price=Decimal("190.00"),
            requires_quote=True,
        )

    def test_configurable_print_product_keeps_options_variant_and_price_rule(self):
        finish = ProductOption.objects.create(product=self.product, name="Finish", code="finish")
        matte = OptionValue.objects.create(option=finish, label="Matte", code="matte", price_modifier=Decimal("0.00"))
        foil = OptionValue.objects.create(option=finish, label="Gold Foil", code="gold-foil", price_modifier=Decimal("200.00"))
        
        variant = ProductVariant.objects.create(product=self.product, sku="CARD-MATTE", price=Decimal("190.00"))
        variant.option_values.add(matte)
        
        rule = PriceRule.objects.create(
            product=self.product,
            minimum_quantity=100,
            unit_price=Decimal("190.00"),
            setup_charge=Decimal("0.00"),
            selected_options={"finish": "matte"}
        )
        self.assertEqual(variant.option_values.get(), matte)
        self.assertEqual(rule.selected_options["finish"], "matte")

    def test_dynamic_price_calculation_with_volume_tiers_and_options(self):
        # Create volume price rules: 100 qty -> ₹190, 500 qty -> ₹600
        PriceRule.objects.create(product=self.product, minimum_quantity=100, unit_price=Decimal("190.00"))
        PriceRule.objects.create(product=self.product, minimum_quantity=500, unit_price=Decimal("600.00"))

        option = ProductOption.objects.create(product=self.product, name="Paper", code="paper")
        val_glossy = OptionValue.objects.create(option=option, label="Glossy", code="glossy", price_modifier=Decimal("50.00"))

        # Price for 100 qty without options = 190.00
        price_100 = self.product.calculate_total_price(quantity=100)
        self.assertEqual(price_100, Decimal("190.00"))

        # Price for 500 qty with glossy (+50) = 600.00 + 50.00 = 650.00
        price_500 = self.product.calculate_total_price(quantity=500, option_value_ids=[val_glossy.id])
        self.assertEqual(price_500, Decimal("650.00"))

    def test_image_url_fallback(self):
        url = self.product.get_image_url
        self.assertTrue(url.endswith(".jpg") or url.endswith(".png") or "/static/" in url)

    def test_product_options_api_endpoint(self):
        PriceRule.objects.create(product=self.product, minimum_quantity=100, unit_price=Decimal("190.00"))
        url = reverse("catalog:product_options_api", kwargs={"product_id": self.product.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["product"]["name"], "Business Cards")
