import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        with open(
            ('/app/data/' + 'ingredients.csv'),
            encoding='utf8'
        ) as file:
            reader = csv.reader(file)
            for row in reader:
                Ingredient.objects.get_or_create(
                    name=row[0],
                    measurement_unit=row[1]
                )
            print('Ингредиенты загружены')
