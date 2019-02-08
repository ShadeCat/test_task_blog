from django.contrib import admin
from . import models

admin.site.site_header = 'Мой блог'

admin.site.register(models.User)
admin.site.register(models.Post)
