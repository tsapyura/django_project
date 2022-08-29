from django import template
from main.models import MenuItem

register = template.Library()


@register.inclusion_tag("main/navbar_menu_items.html")
def all_menu_items():
    # final_url = str(url)
    # if final_url == '/' or final_url == '/about':
    #     all_menu_items_list = MenuItem.objects.exclude(url__endswith='add')
    #     return all_menu_items_list
    # else:
    # all_menu_items_list = MenuItem.objects.order_by("id")
    return {"all_menu_items_list": MenuItem.objects.all()}
