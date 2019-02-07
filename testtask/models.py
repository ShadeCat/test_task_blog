from django.db import models


class Post(models.Model):
    created = models.DateTimeField('создан', auto_now_add=True)
    title = models.CharField('заголовок', max_length=100, unique=True)
    slug = models.SlugField(editable=False, unique=True, db_index=True)
    body = models.TextField('текст', blank=True)

