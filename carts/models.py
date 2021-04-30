from django.db import models
from items.models import Item
from users.models import User


class Cart(models.Model):
    items = models.ManyToManyField('CartItem', verbose_name='продуткы', related_name='items')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='владелец')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='окончательная цена', default=0)
    quantity = models.PositiveIntegerField(verbose_name='кол-во товаров', default=0)
    in_order = models.BooleanField(default=False, verbose_name='состояние')

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'

    def __str__(self):
        return f'Корзина пользователя - {self.user.username}'


class CartItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='продукт')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='корзина', blank=True, null=True,
                             related_name='item')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='цена', blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name='кол-во товаров')

    class Meta:
        verbose_name = 'cart_item'
        verbose_name_plural = 'cart_items'

    def __str__(self):
        return f'cart item - {self.pk}'

    def save(self, *args, **kwargs):
        self.price = int(self.quantity) * self.item.price
        super(CartItem, self).save(*args, **kwargs)
