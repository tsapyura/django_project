from django.urls import path
from .views import add_product, product_details, show_products, edit_product

urlpatterns = [
    path("add", add_product, name="add_product"),
    path("<int:id>", product_details, name="product_details"),
    path("showProducts", show_products, name="show_products"),
    path("edit/<str:pk>", edit_product, name="edit_product")
]
