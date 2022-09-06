from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django_project.settings import STATIC_ROOT
from .forms import UserSignUpForm, UserSignInForm
from .models import MenuItem
from products.models import Product, Category, OrderItem, Order
from django.db.models import Q


def home(request):
    return render(request, 'main/index.html', {'user': request.user, 'url': request.get_full_path})


def sign_up(request):
    form = UserSignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get("password"))
        user = form.save()
        login(request, user)
        return redirect("/")
    return render(request, "main/sign-up.html", {"form": form})


def sign_in(request):
    form = UserSignInForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            request.session["invalid_user"] = True
    return render(request, "main/sign-in.html", {"form": form})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")


def add_to_cart(request, product_id):
    if Product.objects.get(id=product_id):
        if product_id in request.session.get("products", []):
            return redirect("/")
        if request.session.get("products", False):
            request.session["products"].append(product_id)
            request.session.modified = True
        else:
            request.session["products"] = []
            request.session["products"].append(product_id)

        total_price = 0
        for product_id in request.session.get("products", []):
            product_price = Product.objects.get(id=product_id).price
            total_price = total_price + product_price

        request.session["cart_total_price"] = total_price
    else:
        raise Http404()
    return redirect("/products")


def cart(request):
    if request.session.get("products", False):
        products = Product.objects.filter(id__in=request.session.get("products"))
        return render(request, "main/cart.html", {"products": products, "total_price": request.session.get("cart_total_price", 0)})
    else:
        return render(request, "main/cart.html", {})


def remove_from_cart(request, product_id):
    if request.session.get("products", False):
        product_len = len(request.session.get("products"))
        for i in range(product_len):
            if request.session.get("products")[i] == product_id:
                del request.session.get("products")[i]
                request.session.modified = True
                product = Product.objects.get(id=product_id)
                request.session["cart_total_price"] = request.session["cart_total_price"] - product.price
                break
    return redirect("/cart")


def order(request):
    if request.session.get("products", False):
        if request.user.is_authenticated:
            if request.method == "GET":
                return render(request, "main/order.html", {"total_price": request.session.get("cart_total_price", 0)})
            else:
                order = Order()
                order.user = request.user
                order.message = request.POST.get("description")
                order.address = request.POST.get("address")
                order.name = request.POST.get("name")
                order.email = request.POST.get("email")
                order.total_price = request.session.get("cart_total_price")
                order.save()
                for product_id in request.session.get("products", []):
                    order_item = OrderItem()
                    order_item.order = order
                    order_item.product_id = product_id
                    order_item.save()

                # send_mail(
                #     "New Order #" + str(order.id),
                #     "You have new order on the Our Shop \n Message from client: \n" + order.message,
                #     "turupuru8@gmail.com",
                #     ["yuratsap1999@gmail.com"],
                # )
                request.session["products"] = []
                request.session["cart_total_price"] = 0
                return redirect("/")
