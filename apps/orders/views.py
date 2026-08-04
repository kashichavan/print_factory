import json
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from apps.catalog.models import Product, ProductVariant
import time
from .models import Cart, CartItem, Order, OrderItem

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

@csrf_exempt
@require_POST
def checkout(request):
    try:
        cart = _get_cart(request)
        cart_items = cart.items.select_related("product", "variant").all()
        
        if not cart_items.exists():
            return JsonResponse({"success": False, "message": "Your cart is empty. Please add products before checking out."}, status=400)

        customer_name = request.POST.get("customer_name", "").strip()
        customer_email = request.POST.get("customer_email", "").strip()
        customer_phone = request.POST.get("customer_phone", "").strip()
        notes = request.POST.get("notes", "").strip()

        if not customer_name or not customer_email or not customer_phone:
            return JsonResponse({"success": False, "message": "Please fill in your Name, Email, and Mobile Phone Number."}, status=400)

        subtotal = Decimal("0.00")
        for item in cart_items:
            tot = Decimal(item.specifications.get("total_price", "0.00"))
            subtotal += tot

        tax = round(subtotal * Decimal("0.18"), 2)
        shipping = Decimal("0.00") if (subtotal >= Decimal("999.00") or subtotal == Decimal("0.00")) else Decimal("99.00")

        order_number = f"ORD-{int(time.time())}"
        artwork_file = request.FILES.get("artwork_file")

        user = request.user if request.user.is_authenticated else None
        order = Order.objects.create(
            number=order_number,
            customer=user,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            artwork_file=artwork_file,
            subtotal=subtotal,
            tax_amount=tax,
            shipping_amount=shipping,
            notes=notes,
            status=Order.Status.PENDING,
        )

        for item in cart_items:
            unit_p = Decimal(item.specifications.get("unit_price", "0.00"))
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                product_name=item.product.name,
                sku=item.variant.sku if item.variant else "",
                quantity=item.quantity,
                specifications=item.specifications,
                unit_price=unit_p,
            )

        cart.items.all().delete()

        return JsonResponse({
            "success": True,
            "order_number": order.number,
            "message": f"Order #{order.number} placed successfully! It has been automatically sent to the owner."
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

@csrf_exempt
@require_POST
def add_to_cart(request):
    try:
        cart = _get_cart(request)
        
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, TypeError):
            data = request.POST

        product_id = data.get("product_id")
        if not product_id:
            return JsonResponse({"success": False, "message": "Missing product ID"}, status=400)

        quantity = int(data.get("quantity", 100))
        paper = data.get("paper", "Standard")
        corners = data.get("corners", "Standard")
        sides = data.get("sides", "Standard")
        orientation = data.get("orientation", "Horizontal")
        
        raw_price = str(data.get("total_price", "190.00")).replace(",", "").replace("₹", "").strip()
        try:
            calculated_total = Decimal(raw_price)
        except Exception:
            calculated_total = Decimal("190.00")
        
        product = get_object_or_404(Product, id=product_id)
        variant = product.variants.first()

        unit_p = str(round(calculated_total / quantity, 2)) if quantity > 0 else "0.00"

        specifications = {
            "paper": paper,
            "corners": corners,
            "sides": sides,
            "orientation": orientation,
            "unit_price": unit_p,
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
            curr_total = Decimal(cart_item.specifications.get("total_price", "0")) + calculated_total
            cart_item.specifications["total_price"] = str(curr_total)
            cart_item.save()

        total_items = sum(item.quantity for item in cart.items.all())
        cart_count = cart.items.count()

        return JsonResponse({
            "success": True,
            "message": f"Added {quantity} x {product.name} to cart!",
            "cart_count": cart_count,
            "total_items": total_items,
        })
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

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
