# catalog/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Product, Category

class CatalogListTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name="Tech",
            slug="tech",
            description="Categoría de tecnología"
        )
        self.product = Product.objects.create(
            name="Tenis Court Blanco Unisex",
            price_cop=165000,
            is_active=True,
            category=self.category
        )

    def test_catalog_list_loads_and_shows_product(self):
        url = reverse("catalog:list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)