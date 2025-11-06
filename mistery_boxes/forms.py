from django import forms
from .models import MysteryBox
from catalog.models import Product, Category


class MysteryBoxForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Categoría",
        help_text="Selecciona la categoría principal de esta caja",
        widget=forms.Select(attrs={"class": "form-select"})
    )
    products = forms.ModelMultipleChoiceField(
        queryset=Product.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecciona los productos"
    )

    class Meta:
        model = MysteryBox
        fields = [
            "name",
            "slug",
            "description",
            "category",
            "price_cop",
            "image",
            "products"
            ]
