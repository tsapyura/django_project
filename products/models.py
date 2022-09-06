from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, default=False, null=True, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.IntegerField(default=0)
    approved_by = models.ForeignKey(User, related_name="approved_by", null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField(default=False)
    display_on_main_page = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=100, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    parent_id = models.IntegerField(null=True, blank=True)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    message = models.TextField()
    address = models.CharField(max_length=500, default="")
    name = models.CharField(max_length=255, default="")
    email = models.CharField(max_length=255, default="")
    total_price = models.IntegerField()

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.order.id)

