from django.urls import path
from . import views

app_name = "content"
urlpatterns = [
    path("", views.home, name="home"),
    path("business-cards/", views.business_cards, name="business_cards"),
    path("category/<slug:slug>/", views.category_detail, name="category_detail"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("services/", views.services, name="services"),
    path("shop/", views.shop, name="shop"),
    path("contact/", views.contact, name="contact"),
]
