from django import forms
from django.utils.text import slugify
from apps.catalog.models import Category, Product
from apps.orders.models import Order


class ProductForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"accept": "image/*"}))
    product_type = forms.ChoiceField(choices=Product.ProductType.choices, initial=Product.ProductType.PRINT, required=False)
    is_active = forms.BooleanField(initial=True, required=False, label="Publish Live on Storefront")

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "product_type",
            "base_price",
            "badge",
            "image",
            "short_description",
            "description",
            "requires_quote",
            "is_active",
        ]
        widgets = {
            "short_description": forms.TextInput(attrs={"placeholder": "e.g. Clean 300gsm matte or glossy cards"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Detailed product specifications, paper weights, dimensions, and usage instructions..."}),
            "base_price": forms.NumberInput(attrs={"placeholder": "190.00", "step": "0.01"}),
            "badge": forms.TextInput(attrs={"placeholder": "e.g. Bestseller / 3D Foil / 100% Recycled"}),
        }

    def clean_product_type(self):
        pttype = self.cleaned_data.get("product_type")
        return pttype or Product.ProductType.PRINT

    def clean_is_active(self):
        # Default to True when creating a product unless explicitly unchecked
        if "is_active" in self.cleaned_data:
            return self.cleaned_data["is_active"]
        return True

    def save(self, commit=True):
        product = super().save(commit=False)
        product.slug = slugify(product.name)
        base_slug = product.slug
        index = 2
        while Product.objects.exclude(pk=product.pk).filter(slug=product.slug).exists():
            product.slug = f"{base_slug}-{index}"
            index += 1
        if commit:
            product.save()
        return product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "icon", "badge", "description", "is_active"]
        widgets = {
            "icon": forms.TextInput(attrs={"placeholder": "e.g. 💳 / 📦 / 👕"}),
            "badge": forms.TextInput(attrs={"placeholder": "e.g. 50+ Stocks / Custom Sizes"}),
        }

    def save(self, commit=True):
        category = super().save(commit=False)
        category.slug = slugify(category.name)
        if commit:
            category.save()
        return category


class OrderTrackingForm(forms.ModelForm):
    carrier = forms.CharField(max_length=100, required=False)
    tracking_number = forms.CharField(max_length=120, required=False)

    class Meta:
        model = Order
        fields = ["status", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shipment = self.instance.shipments.first()
        if shipment:
            self.fields["carrier"].initial = shipment.carrier
            self.fields["tracking_number"].initial = shipment.tracking_number


class ServiceForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={"accept": "image/*"}))
    is_active = forms.BooleanField(initial=True, required=False, label="Active on Storefront")

    class Meta:
        from apps.content.models import Service
        model = Service
        fields = ["title", "badge", "summary", "body", "tags_csv", "speed_info", "base_rate", "image", "position", "is_active"]
        widgets = {
            "summary": forms.TextInput(attrs={"placeholder": "e.g. Short runs, quick turnarounds and vivid detail"}),
            "tags_csv": forms.TextInput(attrs={"placeholder": "Visiting Cards, Letterheads, Brochures, Catalogues"}),
            "speed_info": forms.TextInput(attrs={"placeholder": "e.g. Same-Day / 24hr Express"}),
        }

    def save(self, commit=True):
        service = super().save(commit=False)
        if not service.slug:
            service.slug = slugify(service.title)
        if commit:
            service.save()
        return service

