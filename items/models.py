from django.db import models

from Boxes.settings import ITEM_IMAGE_DIR


class Item(models.Model):
    title = models.CharField(max_length=30, verbose_name='наименование')
    description = models.TextField(max_length=3000, verbose_name='описание')
    image = models.ImageField(upload_to=ITEM_IMAGE_DIR, verbose_name='картинка')
    weight = models.PositiveIntegerField(verbose_name='вес в граммах')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='цена в рублях')
    size = models.CharField(max_length=30, verbose_name='Размеры', blank=True)

    class Meta:
        verbose_name = 'Коробка'
        verbose_name_plural = 'Коробки'

    def __str__(self):
        return self.title
