from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Product

def product_options_api(request, product_id):
    product = get_object_or_404(
        Product.objects.prefetch_related("options__values", "price_rules"),
        id=product_id,
        is_active=True
    )

    # Format price rules from DB
    price_rules_data = []
    rules = list(product.price_rules.filter(is_active=True).order_by("minimum_quantity"))
    if not rules:
        price_rules_data = [
            {"qty": 100, "price": float(product.base_price), "label": "Standard"},
            {"qty": 250, "price": float(round(product.base_price * Decimal('2.1'), 2)), "label": "Save 18%"},
            {"qty": 500, "price": float(round(product.base_price * Decimal('3.6'), 2)), "label": "Save 35%"},
            {"qty": 1000, "price": float(round(product.base_price * Decimal('5.8'), 2)), "label": "Best Value"},
        ]
    else:
        for r in rules:
            price_rules_data.append({
                "qty": r.minimum_quantity,
                "price": float(r.unit_price) if r.unit_price else float(product.base_price),
                "label": f"Tier ({r.minimum_quantity} units)"
            })

    # Format options & values from DB
    options_data = []
    for opt in product.options.all():
        values_data = []
        for val in opt.values.all().order_by("position"):
            values_data.append({
                "id": str(val.id),
                "label": val.label,
                "code": val.code,
                "price_modifier": float(val.price_modifier)
            })
        options_data.append({
            "id": str(opt.id),
            "name": opt.name,
            "code": opt.code,
            "required": opt.required,
            "values": values_data
        })

    return JsonResponse({
        "success": True,
        "product": {
            "id": str(product.id),
            "name": product.name,
            "slug": product.slug,
            "base_price": float(product.base_price),
            "image_url": product.get_image_url,
            "price_rules": price_rules_data,
            "options": options_data
        }
    })
