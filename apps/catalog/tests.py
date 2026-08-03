from django.test import TestCase
from .models import Category, OptionValue, PriceRule, Product, ProductOption, ProductVariant


class CatalogModelTests(TestCase):
    def test_configurable_print_product_keeps_options_variant_and_price_rule(self):
        category = Category.objects.create(name="Business stationery", slug="business-stationery")
        product = Product.objects.create(name="Business cards", slug="business-cards", category=category, product_type="print", requires_quote=True)
        finish = ProductOption.objects.create(product=product, name="Finish", code="finish")
        matte = OptionValue.objects.create(option=finish, label="Matte", code="matte")
        variant = ProductVariant.objects.create(product=product, sku="CARD-MATTE", price="8.50")
        variant.option_values.add(matte)
        rule = PriceRule.objects.create(product=product, minimum_quantity=100, unit_price="7.00", setup_charge="250.00", selected_options={"finish": "matte"})
        self.assertEqual(variant.option_values.get(), matte)
        self.assertEqual(rule.selected_options["finish"], "matte")
