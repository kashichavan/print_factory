from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.text import slugify

from apps.catalog.models import Category, Product, ProductOption, OptionValue, PriceRule, ProductVariant
from apps.leads.models import ContactInquiry, LeadActivity
from apps.orders.models import Order, Shipment
from apps.production.models import ProductionJob
from .forms import CategoryForm, OrderTrackingForm, ProductForm

staff_required = user_passes_test(lambda user: user.is_staff)


@login_required
@staff_required
def dashboard_home(request):
    status_counts = dict(Order.objects.values_list("status").annotate(total=Count("id")))
    return render(request, "dashboard/home.html", {
        "product_count": Product.objects.count(),
        "new_lead_count": ContactInquiry.objects.filter(status="new").count(),
        "open_order_count": Order.objects.exclude(status__in=["delivered", "cancelled"]).count(),
        "recent_orders": Order.objects.select_related("customer").order_by("-created_at")[:6],
        "status_counts": status_counts,
    })


# --- PRODUCTS CRUD ---

@login_required
@staff_required
def product_list(request):
    qs = Product.objects.filter(is_active=True).select_related("category").prefetch_related("options").order_by("-created_at")
    
    search = request.GET.get("q", "").strip()
    if search:
        qs = qs.filter(name__icontains=search)

    paginator = Paginator(qs, 8)
    page_number = request.GET.get("page", 1)
    products_page = paginator.get_page(page_number)

    return render(request, "dashboard/products.html", {
        "products": products_page,
        "search_query": search,
    })


@login_required
@staff_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        product = form.save()

        _save_dynamic_options(product, request)
        _save_dynamic_price_rules(product, request)

        ProductVariant.objects.get_or_create(
            product=product,
            sku=f"SKU-{product.slug[:10].upper()}",
            defaults={"price": product.base_price, "is_active": True}
        )

        messages.success(request, f"Product '{product.name}' created successfully!")
        return redirect("dashboard:product_list")
        
    return render(request, "dashboard/product_form.html", {
        "form": form,
        "title": "Add New Product",
        "categories": Category.objects.filter(is_active=True),
    })


@login_required
@staff_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    
    if request.method == "POST" and form.is_valid():
        product = form.save()
        
        # Reset & update dynamic options & price rules
        product.options.all().delete()
        product.price_rules.all().delete()
        
        _save_dynamic_options(product, request)
        _save_dynamic_price_rules(product, request)

        messages.success(request, f"Product '{product.name}' updated successfully!")
        return redirect("dashboard:product_list")

    return render(request, "dashboard/product_form.html", {
        "form": form,
        "product": product,
        "title": f"Edit Product: {product.name}",
        "categories": Category.objects.filter(is_active=True),
    })


@login_required
@staff_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        name = product.name
        product.delete()
        messages.success(request, f"Product '{name}' deleted!")
        return redirect("dashboard:product_list")
    return render(request, "dashboard/product_confirm_delete.html", {"product": product})


@login_required
@staff_required
def product_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.is_active = not product.is_active
    product.save()
    status_str = "Activated" if product.is_active else "Deactivated"
    messages.success(request, f"Product '{product.name}' is now {status_str}.")
    return redirect("dashboard:product_list")


def _save_dynamic_options(product, request):
    option_names = request.POST.getlist("dyn_option_name[]")
    option_vals = request.POST.getlist("dyn_option_values[]")
    
    for name, vals_str in zip(option_names, option_vals):
        if name.strip():
            opt_code = slugify(name.strip())[:25]
            opt, _ = ProductOption.objects.get_or_create(
                product=product,
                code=opt_code,
                defaults={"name": name.strip(), "required": True}
            )
            
            val_items = [v.strip() for v in vals_str.split(",") if v.strip()]
            for idx, vitem in enumerate(val_items, start=1):
                if ":" in vitem:
                    vlabel, vmod = vitem.split(":", 1)
                else:
                    vlabel, vmod = vitem, "0"
                
                vlabel = vlabel.strip()
                try:
                    vmod_val = Decimal(vmod.strip() or "0")
                except Exception:
                    vmod_val = Decimal("0.00")
                    
                vcode = slugify(vlabel)[:25]
                OptionValue.objects.get_or_create(
                    option=opt,
                    code=vcode,
                    defaults={"label": vlabel, "price_modifier": vmod_val, "position": idx}
                )


def _save_dynamic_price_rules(product, request):
    min_qtys = request.POST.getlist("tier_min_qty[]")
    unit_prices = request.POST.getlist("tier_unit_price[]")
    
    for q_str, p_str in zip(min_qtys, unit_prices):
        if q_str and p_str:
            try:
                q_val = int(q_str)
                p_val = Decimal(p_str)
                PriceRule.objects.get_or_create(
                    product=product,
                    minimum_quantity=q_val,
                    defaults={"unit_price": p_val, "is_active": True}
                )
            except (ValueError, TypeError):
                pass


# --- CATEGORIES ---

@login_required
@staff_required
def category_create(request):
    form = CategoryForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        cat = form.save()
        messages.success(request, f"Category '{cat.name}' created successfully!")
        return redirect("dashboard:product_create")
    return render(request, "dashboard/category_form.html", {"form": form})


# --- ORDERS & PRODUCTION ---

@login_required
@staff_required
def order_list(request):
    status = request.GET.get("status")
    qs = Order.objects.select_related("customer", "organization").order_by("-created_at")
    if status:
        qs = qs.filter(status=status)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page", 1)
    orders_page = paginator.get_page(page_number)

    return render(request, "dashboard/orders.html", {
        "orders": orders_page,
        "selected_status": status,
        "statuses": Order.Status.choices,
    })


@login_required
@staff_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.select_related("customer", "organization", "billing_address", "shipping_address")
        .prefetch_related("items__product", "payments", "shipments"),
        pk=order_id
    )
    form = OrderTrackingForm(request.POST or None, instance=order)
    
    if request.method == "POST" and form.is_valid():
        order = form.save()
        carrier, tracking = form.cleaned_data["carrier"], form.cleaned_data["tracking_number"]
        if carrier or tracking:
            shipment, _ = Shipment.objects.get_or_create(order=order)
            shipment.carrier, shipment.tracking_number = carrier, tracking
            if order.status == Order.Status.SHIPPED and not shipment.shipped_at:
                shipment.shipped_at = timezone.now()
            if order.status == Order.Status.DELIVERED and not shipment.delivered_at:
                shipment.delivered_at = timezone.now()
            shipment.save()

        if order.status == Order.Status.IN_PRODUCTION:
            ProductionJob.objects.get_or_create(order=order, defaults={"job_number": f"JOB-{order.number}"})
            
        messages.success(request, f"Order {order.number} updated!")
        return redirect("dashboard:order_detail", order_id=order.id)

    return render(request, "dashboard/order_detail.html", {"order": order, "form": form})


# --- LEADS & ENQUIRIES WITH STAFF ATTRIBUTION ---

@login_required
@staff_required
def lead_list(request):
    status = request.GET.get("status")
    qs = ContactInquiry.objects.select_related("assigned_to", "updated_by").prefetch_related("activities__author").order_by("-created_at")
    
    if status:
        qs = qs.filter(status=status)

    paginator = Paginator(qs, 10)
    page_number = request.GET.get("page", 1)
    leads_page = paginator.get_page(page_number)

    return render(request, "dashboard/leads.html", {
        "leads": leads_page,
        "selected_status": status,
        "status_choices": ContactInquiry.Status.choices,
    })


@login_required
@staff_required
def lead_update(request, pk):
    lead = get_object_or_404(ContactInquiry, pk=pk)
    if request.method == "POST":
        new_status = request.POST.get("status")
        reason = request.POST.get("status_reason", "").strip()
        note = request.POST.get("note", "").strip()

        lead.status = new_status
        lead.status_reason = reason
        lead.updated_by = request.user
        lead.save()

        if note:
            LeadActivity.objects.create(
                inquiry=lead,
                author=request.user,
                note=f"Status changed to '{lead.get_status_display()}'. Note: {note}"
            )

        messages.success(request, f"Lead '{lead.name}' updated by {request.user.email}!")
        return redirect("dashboard:lead_list")
        
    return redirect("dashboard:lead_list")


# --- SERVICES MANAGEMENT ---

@login_required
@staff_required
def service_list(request):
    from apps.content.models import Service
    services = Service.objects.all().order_by("position", "title")
    return render(request, "dashboard/services.html", {"services": services})


@login_required
@staff_required
def service_create(request):
    from apps.dashboard.forms import ServiceForm
    form = ServiceForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        srv = form.save()
        messages.success(request, f"Service '{srv.title}' created successfully!")
        return redirect("dashboard:service_list")
    return render(request, "dashboard/service_form.html", {"form": form, "title": "Create New Service"})


@login_required
@staff_required
def service_edit(request, pk):
    from apps.content.models import Service
    from apps.dashboard.forms import ServiceForm
    srv = get_object_or_404(Service, pk=pk)
    form = ServiceForm(request.POST or None, request.FILES or None, instance=srv)
    if request.method == "POST" and form.is_valid():
        srv = form.save()
        messages.success(request, f"Service '{srv.title}' updated!")
        return redirect("dashboard:service_list")
    return render(request, "dashboard/service_form.html", {"form": form, "service": srv, "title": f"Edit Service: {srv.title}"})


@login_required
@staff_required
def service_delete(request, pk):
    from apps.content.models import Service
    srv = get_object_or_404(Service, pk=pk)
    if request.method == "POST":
        title = srv.title
        srv.delete()
        messages.success(request, f"Service '{title}' deleted.")
        return redirect("dashboard:service_list")
    return render(request, "dashboard/service_confirm_delete.html", {"service": srv})

