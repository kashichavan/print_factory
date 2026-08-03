from django.urls import path
from . import views

app_name = "orders"
urlpatterns = [
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/add/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<uuid:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/count/", views.cart_count, name="cart_count"),
]
