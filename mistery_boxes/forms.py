from django import forms
from .models import MysteryBox
from catalog.models import Product


class MysteryBoxForm(forms.ModelForm):
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
            "price_cop",
            "image",
            "products"
            ]
