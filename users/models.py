from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField(max_length=40, verbose_name='отчество')
    phone = models.CharField(max_length=20, verbose_name='телефон')
    address = models.CharField(max_length=40, verbose_name='адрес')
    premium = models.BooleanField(default=False, verbose_name='Премиум')

    class Meta:
        verbose_name = 'Пользоваетль'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'пользоваетль {self.id}'
