from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from apps.catalog.models import Category, Product
from apps.leads.models import ContactInquiry
from .models import Service


def home(request):
    active_cat_slug = request.GET.get("category", "")
    categories = Category.objects.filter(is_active=True).prefetch_related("products")
    
    if active_cat_slug:
        qs = Product.objects.filter(category__slug=active_cat_slug, is_active=True).select_related("category").prefetch_related("options__values", "price_rules").order_by("-created_at")
    else:
        qs = Product.objects.filter(is_active=True).select_related("category").prefetch_related("options__values", "price_rules").order_by("-created_at")

    paginator = Paginator(qs, 8)
    page_number = request.GET.get("page", 1)
    products_page = paginator.get_page(page_number)

    return render(request, "content/home.html", {
        "categories": categories,
        "products": products_page,
        "active_category_slug": active_cat_slug,
        "services": Service.objects.filter(is_active=True)[:3],
    })


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category").prefetch_related("options__values", "price_rules", "images"),
        slug=slug,
        is_active=True
    )
    related_products = Product.objects.filter(category=product.category, is_active=True).exclude(id=product.id).order_by("-created_at")[:4]

    return render(request, "content/product_detail.html", {
        "product": product,
        "related_products": related_products,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    qs = Product.objects.filter(category=category, is_active=True).prefetch_related("options__values", "price_rules").order_by("-created_at")
    all_categories = Category.objects.filter(is_active=True)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page", 1)
    products_page = paginator.get_page(page_number)

    return render(request, "content/category_detail.html", {
        "category": category,
        "products": products_page,
        "all_categories": all_categories,
    })


def business_cards(request):
    return category_detail(request, slug="business-cards")


def shop(request):
    active_cat_slug = request.GET.get("category", "")
    categories = Category.objects.filter(is_active=True)
    
    if active_cat_slug:
        qs = Product.objects.filter(category__slug=active_cat_slug, is_active=True).select_related("category").prefetch_related("options__values").order_by("-created_at")
    else:
        qs = Product.objects.filter(is_active=True).select_related("category").prefetch_related("options__values").order_by("-created_at")

    paginator = Paginator(qs, 12)
    page_number = request.GET.get("page", 1)
    products_page = paginator.get_page(page_number)

    return render(request, "content/shop.html", {
        "categories": categories,
        "products": products_page,
        "active_category_slug": active_cat_slug,
    })


def services(request):
    return render(request, "content/services.html", {"services": Service.objects.filter(is_active=True)})


def contact(request):
    if request.method == "POST":
        ContactInquiry.objects.create(
            name=request.POST.get("name", "").strip(),
            email=request.POST.get("email", "").strip(),
            phone=request.POST.get("phone", "").strip(),
            message=request.POST.get("message", "").strip(),
        )
        messages.success(request, "Thanks — our team will get back to you shortly.")
        return redirect("content:contact")
    return render(request, "content/contact.html")


def about(request):
    return render(request, "content/about.html")
