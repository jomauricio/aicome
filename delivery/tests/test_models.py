from django.test import TestCase
from ..models import Restaurante, Pedido
from address.models import Address

# Create your tests here.

class RestauranteTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        Address.objects.create(raw='Rua Pires de Castro, 1129')

    def setUp(self):
        # Setup run before every test method.
        pass


    def tearDown(self):
        # Clean up run after every test method.
        pass

    def test_restaurante_create(self):
        add = Address.objects.first()
        restaurante = Restaurante(nome='Casa da Coxinha', endereco=add, fone='9898989')
        restaurante.save()
        restaurante_bd = Restaurante.objects.get(id=restaurante.id)
        self.assertEqual(restaurante, restaurante_bd)