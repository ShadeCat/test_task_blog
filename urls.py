
from django.contrib import admin
from django.urls import path
from testtask.views import *

urlpatterns = [
    path('', IndexView.as_view()),
    path('admin/', admin.site.urls),
    path('myblog/', MyBlogView.as_view()),
    path('authors/', AuthorsView.as_view()),
]
