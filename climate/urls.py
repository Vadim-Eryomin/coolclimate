"""
URL configuration for climate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from router import views
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = (
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + [
        path("admin/", admin.site.urls),
        #
        path("cards", views.choose_category_for_cards),
        path("cards/<int:category_id>", views.get_all_cards),
        path("cards/<int:category_id>/new", views.new_card),
        path("cards/<int:category_id>/<int:card_id>", views.check_card),
        path("cards/<int:category_id>/<int:card_id>/edit_card", views.edit_card),
        path("cards/<int:category_id>/<int:card_id>/delete_card", views.delete_card),
        path("cards/<int:category_id>/<int:card_id>/new_variant", views.new_variant),
        path("cards/<int:category_id>/<int:card_id>/edit_variant", views.edit_variant),
        path(
            "cards/<int:category_id>/<int:card_id>/delete_variant", views.delete_variant
        ),
        path("cards/<int:category_id>/<int:card_id>/new_image", views.new_image),
        path("cards/<int:category_id>/<int:card_id>/delete_image", views.delete_image),
        path(
            "cards/<int:category_id>/<int:card_id>/edit_filter",
            views.edit_card_filter_value,
        ),
        #
        path("filters", views.choose_category_for_filters),
        path("filters/<int:category_id>", views.get_all_filters),
        path("filters/<int:category_id>/new", views.new_filter),
        path("filters/<int:category_id>/<int:filter_id>", views.check_filter),
        path(
            "filters/<int:category_id>/<int:filter_id>/edit_filter", views.edit_filter
        ),
        path(
            "filters/<int:category_id>/<int:filter_id>/delete_filter",
            views.delete_filter,
        ),
        #
        path("certificates", views.get_all_certificates),
        path("cards/<int:cert_id>", views.get_certificate),
        #
        path("orders", views.all_orders_by_statuses),
        path("orders/all/<str:title>", views.status_orders),
        path("orders/track/<str:track>/change", views.change_order_status),
        path("orders/track/<str:track>", views.admin_track_order),
        #
        path("categories", views.get_all_categories),
        re_path("^create_category", views.create_category),
        re_path("^delete_category", views.delete_category),
        re_path("^edit_category", views.edit_category),
        #
        path("card/<int:card_id>", views.card_data),
        path("add_cart", views.add_to_card),
        path("cart", views.cart),
        path("cart_delete", views.delete_cart),
        path("create_order", views.check_order_correctness),
        path("make_order", views.make_order),
        path("check_order", views.check_order),
        #
        path("register", views.register_page),
        path("register_account", views.register_account),
        path("login", views.login_page),
        path("login_account", views.login_account),
        path("logout", views.logout_account),
        path("change_password", views.change_password),
        #
        path("fill_profile", views.fill_account),
        path("create_profile", views.create_account),
        path("edit_profile_data", views.edit_profile),
        #
        path("profile", views.show_profile),
        path("about", views.about),
        path("", views.index),
    ]
)
