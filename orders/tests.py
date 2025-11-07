from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from catalog.models import Product

User = get_user_model()

class AddToCartTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="beto8", password="1234")
        self.client.login(username="beto8", password="1234")

        self.product = Product.objects.create(
            name="Buzo Técnico Media Capa Hombre",
            price_cop=135000,
            is_active=True
        )

    def test_add_product_to_cart(self):
        """Verifica que agregar al carrito funcione correctamente"""
        url = reverse("orders:add_to_cart")
        response = self.client.post(url, {
            "type": "product",
            "id": self.product.id,
            "qty": "1",
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "cart" in response.content.decode().lower(),
            "No se encontró la palabra 'cart' en la respuesta"
        )
        self.assertContains(response, self.product.name)