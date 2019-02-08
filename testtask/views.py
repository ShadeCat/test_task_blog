from django.views.generic import ListView
from testtask.models import Post


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'testtask/index.html'
