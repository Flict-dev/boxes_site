from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from items.models import Item
from reviews.models import Reviews
from users.models import User
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
        response_item = requests.get(
            'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/foodboxes.json'
        )
        if response_item.status_code == 200:
            json_data_items = response_item.json()
            for item in json_data_items:
                title = item['title']
                Item.objects.update_or_create(
                    title=item['title'],
                    description=item['description'],
                    image=item['image'],
                    weight=item['weight_grams'],
                    size=item['size'],
                    price=item['price']
                )
                print(f'success -{title}')
        else:
            print('URL (items) не поддерживается!')
