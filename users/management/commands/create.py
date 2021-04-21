from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from items.models import Item
from reviews.models import Reviews
from users.models import User
import requests


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('model_name', type=str, help='Название модели [item, user, review]')

    def handle(self, *args, **options):
        model_name = options.get('model_name', None)
        model_name = model_name.lower()
        if model_name is None:
            print('Передайте имя модели, которую хотели бы создать')
        elif model_name == 'user':
            response_user = requests.get(
                'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/recipients.json'
            )
            if response_user.status_code == 200:
                user_json_data = response_user.json()
                for user in user_json_data:
                    username = user['email']
                    User.objects.update_or_create(
                        username=username.split('@')[0],
                        password=user['password'],
                        first_name=user['info']['name'],
                        last_name=user['info']['surname'],
                        middle_name=user['info']['patronymic'],
                        email=user['email'],
                        phone=user['contacts']['phoneNumber'],
                        premium=user['premium'],
                        address=user['city_kladr']
                    )
            else:
                print('URL (users) не поддерживается!')
        elif model_name == 'item':
            response_item = requests.get(
                'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/foodboxes.json'
            )
            if response_item.status_code == 200:
                json_data_items = response_item.json()
                for item in json_data_items:
                    Item.objects.update_or_create(
                        title=item['title'],
                        description=item['description'],
                        image=item['image'],
                        weight=item['weight_grams'],
                        size=item['size'],
                        price=item['price']
                    )
            else:
                print('URL (items) не поддерживается!')

        elif model_name == 'review':
            response_review = requests.get(
                'https://raw.githubusercontent.com/stepik-a-w/drf-project-boxes/master/reviews.json'
            )
            if response_review.status_code == 200:
                json_data_review = response_review.json()
                for review in json_data_review:
                    try:
                        Reviews.objects.update_or_create(
                            text=review['content'],
                            author_id=review['author'],
                            created_at=review['created_at'],
                            published_at=review['published_at'],
                            status=review['status']
                        )
                    except ValidationError:
                        Reviews.objects.update_or_create(
                            text=review['content'],
                            author_id=review['author'],
                            created_at=review['created_at'],
                            published_at='2021-01-03',
                            status=review['status']
                        )
            else:
                print('URL (reviews) не поддерживается!')
