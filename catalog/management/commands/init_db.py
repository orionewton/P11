import requests

from django.core.management.base import BaseCommand
from django.db.utils import DataError, IntegrityError
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Initializes the database'

    CATEGORIES = [
        'Apéritif',
        'Snacks salés',
        'Viandes',
        'Produits à tartiner',
        'Boissons aux fruits',
        'Poissons',
        'Chocolats',
        'Pains',
        'Jambons',
        'Confiseries chocolatées',
        'Soupes'
    ]

    def create_db(self):
        i = 0
        for category in self.CATEGORIES:
            new_category = Category.objects.create(name=category)
            params = {
                'action': 'process',
                'json': 1,
                'page_size': 200,
                'page': 1,
                'tagtype_0': 'categories',
                'tag_contains_0': 'contains',
                'tag_0': category,
            }

            response = requests.get(
                'https://fr.openfoodfacts.org/cgi/search.pl', params=params)

            data = response.json()
            products = data['products']
            for product in products:
                try:
                    name = product["product_name"]
                    brand = product["brands"]
                    nutrition_grade = product["nutrition_grades"]
                    url = product["url"]
                    picture = product['image_front_url']
                    nutrition_image = product["image_nutrition_small_url"]

                    Product.objects.create(
                        name=name,
                        category=new_category,
                        brand=brand,
                        nutrition_grade=nutrition_grade,
                        url=url,
                        picture=picture,
                        nutrition_image=nutrition_image)
                    i += 1

                except KeyError:
                    pass

                except DataError:
                    pass

                except IntegrityError:
                    pass
        print(i, " products add in DB")

    def handle(self, *args, **options):
        self.create_db()
