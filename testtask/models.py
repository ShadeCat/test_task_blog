from django.db import models
from django.contrib.auth.models import AbstractUser
from pytils.translit import slugify


class User(AbstractUser):
    """

    У пользователя есть персональная лента новостей,
    в которой в обратном хронологическом порядке выводятся
    посты из блогов, на которые он подписан.

    При добавлении/удалении подписки содержание ленты меняется (при
    удалении подписки пометки о "прочитанности" сохранять не нужно).
    """
    subscribe = models.ManyToManyField(
        'self',
        related_name='user',
        verbose_name='подписки',
        blank=True,
    )
    """Пользователь может помечать посты в ленте прочитанными."""
    read = models.ManyToManyField(
        'testtask.Post',
        related_name='user',
        verbose_name='прочитано',
        blank=True,
    )

    class Meta(AbstractUser.Meta):
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Post(models.Model):
    created = models.DateTimeField('создан', auto_now_add=True)
    title = models.CharField('заголовок', max_length=100, unique=True)
    body = models.TextField('текст', blank=True)
    slug = models.SlugField(editable=False, unique=True, db_index=True)
    author = models.ForeignKey(
        related_name='post',
        verbose_name='автор',
        on_delete=models.PROTECT,
        to='testtask.User',
    )

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['-created']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.name = self.title.strip()
        self.slug = slugify(self.title)
        """
        При добавлении поста в ленту — подписчики получают почтовое уведомление со
        ссылкой на новый пост. Изменение содержания лент подписчиков (и рассылка уведомлений) д
        олжно происходить как при стандартной публикации поста пользователем
        через интерфейс сайта, так при добавлении/удалении поста через админку.
        """
        super().save(*args, **kwargs)
