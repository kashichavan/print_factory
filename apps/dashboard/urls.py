from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

app_name = "dashboard"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(template_name="dashboard/login.html", redirect_authenticated_user=True), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.dashboard_home, name="home"),
    
    # Products CRUD
    path("products/", views.product_list, name="product_list"),
    path("products/new/", views.product_create, name="product_create"),
    path("products/<uuid:pk>/edit/", views.product_edit, name="product_edit"),
    path("products/<uuid:pk>/delete/", views.product_delete, name="product_delete"),
    path("products/<uuid:pk>/toggle/", views.product_toggle, name="product_toggle"),
    
    # Services CRUD
    path("services/", views.service_list, name="service_list"),
    path("services/new/", views.service_create, name="service_create"),
    path("services/<uuid:pk>/edit/", views.service_edit, name="service_edit"),
    path("services/<uuid:pk>/delete/", views.service_delete, name="service_delete"),

    # Categories
    path("categories/new/", views.category_create, name="category_create"),
    
    # Orders & Production
    path("orders/", views.order_list, name="order_list"),
    path("orders/<uuid:order_id>/", views.order_detail, name="order_detail"),
    
    # Leads & Customer Enquiries
    path("leads/", views.lead_list, name="lead_list"),
    path("leads/<uuid:pk>/update/", views.lead_update, name="lead_update"),
]
