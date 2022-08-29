from django import template
from products.models import Category

register = template.Library()


@register.inclusion_tag("category_nav.html")
def all_categories(category):
    if category == None:
        return {"all_categories_list": Category.objects.filter(parent_id=None).order_by("-id")}
    else:
        category_id = category.id
        return {"all_categories_list": Category.objects.filter(parent_id=category_id).order_by("-id")}


@register.inclusion_tag("category_nav.html")
def current_category():
    return {"all_categories_list": Category.objects.filter(parent_id=None).order_by("-id")}
