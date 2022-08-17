from django.test import TestCase
from django.urls import reverse

from ..models import Restaurante, Pedido
from address.models import Address

# class RestauranteListViewTest(TestCase):

    # def test_view_url_exists_at_desired_location(self):
    #     response = self.client.get('/delivery/restaurantes/')
    #     self.assertEqual(response.status_code, 200)

    # def test_view_uses_correct_template(self):
    #     response = self.client.get(reverse('restaurante-listar'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'restaurante/listar.html')