from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path("api/product/<uuid:product_id>/options/", views.product_options_api, name="product_options_api"),
]
