from .models import Category

def categories_processor(request):
    try:
        categories = Category.objects.filter(is_active=True).order_by("name")
    except Exception:
        categories = []
    return {
        "nav_categories": categories
    }
