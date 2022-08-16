from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404

from products.forms import ProductForm
from products.models import Product, Category


def add_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ProductForm()

    context = {
        "form": form
    }

    return render(request, 'products/add.html', context)

    # if request.user.is_authenticated:
    #     if request.method == "GET":
    #         return render(request, "products/add.html")
    #     else:
    #         product = Product()
    #         product.title = request.POST.get("title")
    #         product.description = request.POST.get("description")
    #         product.user = request.user
    #         product.save()
    #         return render(request, "main/index.html")
    # else:
    #     return redirect("/")


def product_details(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "products/details.html", {"product": product})


def show_products(request):
    category = request.GET.get('category')

    if category == None:
        products = Product.objects.filter(display_on_main_page=True, approved=True).order_by("-id")
        # page_num = request.GET.get("page")
        # paginator = Paginator(products, 2)
        # try:
        #     products = paginator.page(page_num)
        # except PageNotAnInteger:
        #     products = paginator.page(1)
        # except EmptyPage:
        #     products = paginator.page(paginator.num_pages)
    else:
        products = Product.objects.filter(category__name=category)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories
    }

    return render(request, "products/showProducts.html", context)


def edit_product(request, pk):
    if request.user.is_authenticated:
        product = Product.objects.get(id=pk)
        form = ProductForm(instance=product)
        if product.user == request.user:
            if request.method == 'POST':
                form = ProductForm(request.POST, instance=product)
                if form.is_valid():
                    form.save()
                    return redirect('/')

            context = {'form': form}
            return render(request, 'products/edit.html', context)
        else:
            return HttpResponseForbidden()
    else:
        return redirect('/')

    # if request.user.is_authenticated:
    #     product = get_object_or_404(Product, id=id)
    #     if product.user == request.user:
    #         if request.method == 'POST':
    #             form = ProductForm(request.POST, request.FILES)
    #             if form.is_valid():
    #                 form.save()
    #                 return redirect('/')
    #         else:
    #             return redirect('/')
    #     else:
    #         return HttpResponseForbidden()
    #     context = {
    #         "form": form
    #     }
    # return render(request, 'products/edit.html', context)

    # if request.user.is_authenticated:
    #     product = get_object_or_404(Product, id=id)
    #     if product.user == request.user:
    #         if request.method == "POST":
    #             product.title = request.POST.get("title")
    #             product.description = request.POST.get("description")
    #             product.user = request.user
    #             product.save()
    #             return redirect("/")
    #         else:
    #             return render(request, "products/edit.html", {"product": product})
    #     else:
    #         return HttpResponseForbidden()
    # else:
    #     return redirect("/")
