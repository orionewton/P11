from django.test import TestCase
from django.urls import reverse
from .models import Product, Category

# Create your tests here.


class IndexPageTestCase(TestCase):

    def test_index_returns_200(self):
        response = self.client.get(reverse('catalog:index'))
        self.assertEqual(response.status_code, 200)


class DataTests(TestCase):

    def setUp(self):
        pizzas = Category.objects.create(name='pizzas')

        Product.objects.create(
                            name='Pizza',
                            category=pizzas,
                            brand='casino',
                            nutrition_grade='a',
                            picture='www.pizzajpeg.com',
                            nutrition_image='www.pizzanutrigrade.com',
                            url='www.pizza.com')

    def test_search_returns_200(self):
        pizza = str('Pizza')
        response = self.client.get(reverse('catalog:search'), {
            'query': pizza,
        })
        self.assertEqual(response.status_code, 200)

    def test_search_page_redirect_302(self):
        pizza = str('invalid name')
        response = self.client.get(reverse('catalog:search'), {
            'query': pizza,
        })
        self.assertEqual(response.status_code, 302)

    def test_details(self):
        pizza = Product.objects.get(name='Pizza')
        response = self.client.get(reverse('catalog:product_detail',  args=[pizza.id]))
        self.assertEqual(response.status_code, 200)
