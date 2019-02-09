from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from testtask.views import *

urlpatterns = [
    path('', IndexView.as_view()),
    path('admin/', admin.site.urls),
    path('myblog/<str:author>/', MyBlogView.as_view()),
    path('authors/', AuthorsView.as_view()),
    path('log_out/', logout_view),
    path('accounts/', include('django.contrib.auth.urls')),
    path('newpost/', post_new, name='new_post'),
    path('lenta/', LentaView.as_view()),
]
