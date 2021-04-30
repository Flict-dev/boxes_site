from django.core.exceptions import ValidationError
from django.core.management import BaseCommand

from items.models import Item
from reviews.models import Reviews
from users.models import User
import requests


class Command(BaseCommand):
    def handle(self, *args, **options):
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
                print(f'success - {username}')
        else:
            print('URL (users) не поддерживается!')
