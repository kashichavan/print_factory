import json
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from apps.catalog.models import Product, ProductVariant
from .models import Cart, CartItem

def _get_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    user = request.user if request.user.is_authenticated else None
    
    if user:
        cart, _ = Cart.objects.get_or_create(customer=user, is_active=True)
    else:
        cart, _ = Cart.objects.get_or_create(session_key=session_key, is_active=True)
    return cart

@require_POST
def add_to_cart(request):
    cart = _get_cart(request)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        data = request.POST

    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 100))
    paper = data.get("paper", "Standard Matte (300gsm)")
    corners = data.get("corners", "Square")
    sides = data.get("sides", "Front Only")
    orientation = data.get("orientation", "Horizontal")
    calculated_total = Decimal(str(data.get("total_price", "190.00")))
    
    product = get_object_or_404(Product, id=product_id)
    variant = product.variants.first()

    specifications = {
        "paper": paper,
        "corners": corners,
        "sides": sides,
        "orientation": orientation,
        "unit_price": str(round(calculated_total / quantity, 2)),
        "total_price": str(calculated_total),
    }

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
        defaults={"quantity": quantity, "specifications": specifications}
    )
    if not created:
        cart_item.quantity += quantity
        # update specs total
        curr_total = Decimal(cart_item.specifications.get("total_price", "0")) + calculated_total
        cart_item.specifications["total_price"] = str(curr_total)
        cart_item.save()

    total_items = sum(item.quantity for item in cart.items.all())
    cart_count = cart.items.count()

    return JsonResponse({
        "success": True,
        "message": f"Added {quantity} x {product.name} to your cart!",
        "cart_count": cart_count,
        "total_items": total_items,
    })

def cart_detail(request):
    cart = _get_cart(request)
    items = cart.items.select_related("product").all()
    
    subtotal = Decimal("0.00")
    for item in items:
        tot = Decimal(item.specifications.get("total_price", "0.00"))
        subtotal += tot

    tax = round(subtotal * Decimal("0.18"), 2)
    shipping = Decimal("0.00") if subtotal >= Decimal("999.00") or subtotal == Decimal("0.00") else Decimal("99.00")
    grand_total = subtotal + tax + shipping

    context = {
        "cart": cart,
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "shipping": shipping,
        "grand_total": grand_total,
    }
    return render(request, "content/cart.html", context)

@require_POST
def remove_from_cart(request, item_id):
    cart = _get_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    return redirect("orders:cart_detail")

def cart_count(request):
    cart = _get_cart(request)
    return JsonResponse({"cart_count": cart.items.count()})
