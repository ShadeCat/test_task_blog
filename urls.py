
from django.contrib import admin
from django.urls import path
from testtask.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', IndexView.as_view())
]
