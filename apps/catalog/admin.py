from django.contrib import admin
from .models import Category, Product, ProductImage, ProductOption, OptionValue, ProductVariant, PriceRule

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1

class PriceRuleInline(admin.TabularInline):
    model = PriceRule
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "icon", "badge", "is_active"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "base_price", "rating", "review_count", "badge", "is_active"]
    list_filter = ["category", "is_active", "product_type"]
    search_fields = ["name", "description"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductOptionInline, PriceRuleInline]

admin.site.register(ProductOption)
admin.site.register(OptionValue)
admin.site.register(ProductVariant)
admin.site.register(PriceRule)
