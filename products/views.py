from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseForbidden, Http404
from django.shortcuts import render, redirect, get_object_or_404

from products.forms import ProductForm
from products.models import Product, Category


def product_home(request):
    products = Product.objects.order_by("title")
    categories = Category.objects.order_by("-id")

    return render(request, 'products/all_products.html', {
        "products": products,
        'categories': categories,
        'category': None
    })


def add_product(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            categories = Category.objects.order_by("-id")
            form = ProductForm(initial={
                "user": request.user
            })
            return render(request, "products/add.html", {"form": form, "categories": categories})
        else:
            form = ProductForm(request.POST)
            if form.is_valid():
                product = form.save(user=request.user)
                if request.POST.getlist("categories", False):
                    print(request.POST.getlist("categories"))
                    for category_id in request.POST.getlist("categories"):
                        category_id = int(category_id)
                        category = Category.objects.get(id=category_id)
                        category.products.add(product)
                return redirect("/")
            else:
                return render(request, "products/add.html", {"form": form})

    else:
        return redirect("/")


def delete_product(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(id=pk)
        if product.user == request.user:
            if request.method == 'POST':
                product.delete()
                return redirect('/')
            context = {'product': product}
            return render(request, 'products/delete.html', context)
        else:
            return HttpResponseForbidden()
    else:
        return redirect('/')


def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "products/details.html", {"product": product})


def edit_product(request, id):
    if request.user.is_authenticated:
        product = Product.objects.get(id=id)
        if request.user.id == product.user.id:
            if request.method == "GET":
                categories = Category.objects.order_by("-id")
                print("---------------")
                print(categories)
                return render(request, "products/update.html", {
                    'categories': categories,
                    'product': product
                })
            else:
                product.title = request.POST.get("title")
                product.description = request.POST.get("description")
                product.save()
                if request.POST.getlist("category", False):
                    print(request.POST.getlist("category"))
                    for category_id in request.POST.getlist("category"):
                        category_id = int(category_id)
                        category = Category.objects.get(id=category_id)
                        category.products.add(product)
                return redirect("/")
        else:
            return render(request, '404.html')
    else:
        return redirect("/")


def add_category(request):
    if request.user.is_authenticated and request.user.is_staff:
        if request.method == "POST":
            if request.POST.get("title"):
                category = Category()
                category.user = request.user
                category.title = request.POST.get("title")
                default_slug = request.POST.get("title")
                default_slug_2 = default_slug.replace(' ', '-')

                if request.POST.get("parent_category") is not None:
                    category.parent_id = int(request.POST.get("parent_category"))
                    parent_category = Category.objects.get(id=category.parent_id)
                    print(parent_category)
                    final_slug = parent_category.slug + '-' + default_slug_2.lower()
                else:
                    final_slug = default_slug_2.lower()

                category.slug = final_slug
                category.save()
                return redirect("/")
        else:
            categories = Category.objects.order_by("-id")
            return render(request, "products/category/add.html", {"categories": categories})
    else:
        return render(request, '404.html')


def category_page(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        categories = Category.objects.order_by("id")
    except Category.DoesNotExist:
        raise Http404()
    return render(request, "products/all_products.html", {"products": category.products.all(),
                                                          'category': category,
                                                          'categories': categories,
                                                          'category_id': category,
                                                          'current_slug': slug})
