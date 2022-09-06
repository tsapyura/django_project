from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    def save(self, commit=True, **kwargs):
        instance = super(ProductForm, self).save(commit=False)
        instance.user = kwargs["user"]
        if instance.approved:
            instance.approved_by = instance.user
        if commit:
            instance.save()
        return instance

    class Meta:
        model = Product
        fields = ['title', 'description', 'approved', 'display_on_main_page', 'price']
