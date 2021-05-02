from django.core.management import BaseCommand

from items.models import Item
import requests


def download_image(url, name):
    response = requests.get(url)
    out = open(f"media/items/{name}.jpg", "wb")
    out.write(response.content)
    out.close()
    return f'items/{name}.jpg'


class Command(BaseCommand):
    def handle(self, *args, **options):
        response_item = requests.get(
            'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/foodboxes.json'
        )
        if response_item.status_code == 200:
            json_data_items = response_item.json()
            for item in json_data_items:
                title = item['title']
                img_url = item['image']
                Item.objects.update_or_create(
                    title=item['title'],
                    description=item['description'],
                    image=download_image(img_url, title),
                    weight=item['weight_grams'],
                    size=item['size'],
                    price=item['price']
                )
                print(f'success -{title}')
        else:
            print('URL (items) не поддерживается!')
