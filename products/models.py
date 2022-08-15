from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, default=False, null=True, on_delete=models.CASCADE)
    description = models.TextField()
    approved_by = models.ForeignKey(User, related_name="approved_by", null=True, on_delete=models.SET_NULL)
    approved = models.BooleanField(default=False)
    display_on_main_page = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=False, null=True)

    def __str__(self):
        return self.title
