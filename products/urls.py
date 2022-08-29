from django.urls import path
from .views import add_product, product_details, edit_product, delete_product, category_page, \
    add_category, product_home

urlpatterns = [
    path("", product_home, name="product_home"),
    path("/add", add_product, name="add_product"),
    path("/<int:id>", product_details, name="product_details"),
    path("/update/<int:id>", edit_product, name="edit_product"),
    path("/delete_product/<str:pk>", delete_product, name="delete_product"),
    path("/category/<str:slug>", category_page, name="category_page"),
    path("/category/add", add_category, name="add_category"),

]
