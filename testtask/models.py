from django.db import models
from django.contrib.auth.models import AbstractUser



class User(AbstractUser):
    subscribe = models.ManyToManyField(
        'self',
        related_name='user',
        verbose_name='подписки',
        blank=True,
    )

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

