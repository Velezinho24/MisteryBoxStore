from django import forms
from django.utils.translation import gettext_lazy as _

TAG_CHOICES = [
    ("ropa", _("Clothing")),
    ("tecnologia", _("Tech")),
    ("zapatos", _("Shoes")),
    ("deportivo", _("Sport")),
    ("gamer", _("Gamer")),
    ("hombre", _("Men")),
    ("mujer", _("Women")),
    ("unisex", _("Unisex")),
    ("outdoor", _("Outdoor")),
    ("casual", _("Casual")),
    ("premium", _("Premium")),
    ("running", _("Running")),
    ("training", _("Training")),
]

ORDER_CHOICES = [
    ("relevance", _("Relevance")),
    ("price_asc", _("Price: Low to High")),
    ("price_desc", _("Price: High to Low")),
    ("name_asc", _("Name A–Z")),
    ("name_desc", _("Name Z–A")),
]


class CatalogFilterForm(forms.Form):
    """Filter/search form for the product catalog (GET)."""
    q = forms.CharField(
        required=False,
        label=_("Search"),
        widget=forms.TextInput(attrs={
            "class": "form-control bg-black text-white border-secondary",
            "placeholder": _("Search products…"),
        }),
    )
    tags = forms.MultipleChoiceField(
        required=False,
        choices=TAG_CHOICES,
        label=_("Tags"),
        widget=forms.CheckboxSelectMultiple(attrs={
            "class": "form-check-input"
        }),
    )
    price_min = forms.IntegerField(
        required=False,
        label=_("Min price (COP)"),
        min_value=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control bg-black text-white border-secondary",
            "placeholder": _("Min"),
            "inputmode": "numeric",
        }),
    )
    price_max = forms.IntegerField(
        required=False,
        label=_("Max price (COP)"),
        min_value=0,
        widget=forms.NumberInput(attrs={
            "class": "form-control bg-black text-white border-secondary",
            "placeholder": _("Max"),
            "inputmode": "numeric",
        }),
    )
    order = forms.ChoiceField(
        required=False,
        choices=ORDER_CHOICES,
        initial="relevance",
        label=_("Order by"),
        widget=forms.Select(attrs={
            "class": "form-select bg-black text-white border-secondary",
        }),
    )
