from django import forms

from .models import Product, Category


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = ['title', 'category', 'description']
        # category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(),
        #                                           widget=forms.CheckboxSelectMultiple)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),

        }
        labels = {
            'title': 'Enter Product Title:',
            'category': 'Select Category: ',
            'description': 'Enter a Description: ',
        }
