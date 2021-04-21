from django.db import models

from users.models import User


class Reviews(models.Model):
    STATUS_CHOICES = (
        ('new', 'на модерации'),
        ('published', 'опубликован'),
        ('hidden', 'отклонен'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор', related_name='review_author')
    text = models.TextField(max_length=2000, verbose_name='текст отзыва')
    created_at = models.DateField(auto_now=True, verbose_name='Дата создания')
    published_at = models.DateField(verbose_name='Дата публикации')
    status = models.CharField(choices=STATUS_CHOICES, default="new", max_length=30)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв номер - {self.pk}"
