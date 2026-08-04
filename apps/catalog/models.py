from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from apps.core.models import PublishableModel, TimeStampedUUIDModel

class Category(PublishableModel):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="children")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="catalog/categories/", blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, default="")
    badge = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(PublishableModel):
    class ProductType(models.TextChoices):
        PRINT = "print", "Print product"
        GIFT = "gift", "Corporate gift"
        READY = "ready", "Ready product"

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    product_type = models.CharField(max_length=16, choices=ProductType.choices, default=ProductType.PRINT)
    short_description = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="catalog/products/", blank=True, null=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("190.00"))
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=Decimal("4.9"))
    review_count = models.PositiveIntegerField(default=128)
    badge = models.CharField(max_length=60, blank=True, default="Bestseller")
    requires_quote = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["is_active", "category"]),
            models.Index(fields=["product_type"]),
        ]

    def __str__(self):
        return self.name

    def calculate_total_price(self, quantity=100, option_value_ids=None):
        """
        Calculates subtotal based on active volume PriceRules and OptionValue price modifiers.
        Follows SaaS tier-based dynamic pricing principles.
        """
        try:
            quantity = max(1, int(quantity))
        except (ValueError, TypeError):
            quantity = 100

        matching_rule = self.price_rules.filter(is_active=True, minimum_quantity__lte=quantity).order_by("-minimum_quantity").first()
        if matching_rule and matching_rule.unit_price:
            subtotal = matching_rule.unit_price
        else:
            if quantity >= 1000:
                mult = Decimal("5.8")
            elif quantity >= 500:
                mult = Decimal("3.6")
            elif quantity >= 250:
                mult = Decimal("2.1")
            else:
                mult = Decimal("1.0")
            subtotal = self.base_price * mult

        if option_value_ids:
            mods = OptionValue.objects.filter(id__in=option_value_ids).aggregate(total_mod=models.Sum("price_modifier"))["total_mod"]
            if mods:
                subtotal += mods

        return subtotal.quantize(Decimal("0.01"))

    @property
    def get_image_url(self):
        if self.image:
            url_str = str(self.image)
            if url_str.startswith("http://") or url_str.startswith("https://") or url_str.startswith("/"):
                return url_str
            elif url_str.startswith("images/"):
                return f"/static/{url_str}"
            try:
                return self.image.url
            except Exception:
                return f"/static/{url_str}"
        first_img = self.images.first()
        if first_img and first_img.image:
            try:
                return first_img.image.url
            except Exception:
                return f"/static/{first_img.image}"
        return "/static/images/trending-cards-perspective.jpg"

class ProductImage(TimeStampedUUIDModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="catalog/products/")
    alt_text = models.CharField(max_length=255, blank=True)
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["position"]

class ProductOption(TimeStampedUUIDModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="options")
    name = models.CharField(max_length=100) # e.g. Size, Material, Finish, Color
    code = models.SlugField()
    required = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["product", "code"], name="unique_product_option_code")]

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class OptionValue(TimeStampedUUIDModel):
    option = models.ForeignKey(ProductOption, on_delete=models.CASCADE, related_name="values")
    label = models.CharField(max_length=120)
    code = models.SlugField()
    price_modifier = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    position = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["option", "code"], name="unique_option_value_code")]

    def __str__(self):
        return f"{self.label} (+₹{self.price_modifier})" if self.price_modifier > 0 else self.label

class ProductVariant(PublishableModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    sku = models.CharField(max_length=80, unique=True)
    option_values = models.ManyToManyField(OptionValue, blank=True, related_name="variants")
    price = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    compare_at_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    stock_quantity = models.IntegerField(default=0)

class PriceRule(TimeStampedUUIDModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="price_rules")
    minimum_quantity = models.PositiveIntegerField(default=1)
    maximum_quantity = models.PositiveIntegerField(blank=True, null=True)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    setup_charge = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    selected_options = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [models.Index(fields=["product", "is_active", "minimum_quantity"])]
