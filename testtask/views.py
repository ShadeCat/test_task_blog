from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from testtask.models import *
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login


class LoginFormPerform:
    pass


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'testtask/news.html'


class AuthorsView(ListView):
    model = User
    context_object_name = 'authors'
    template_name = 'testtask/authors.html'


class MyBlogView(View):
    template = 'testtask/my_blog.html'

    def get(self, request):
        current_user_name = request.user.get_username()
        current_user_id = User.objects.filter(username=current_user_name)[0].id
        posts = Post.objects.filter(author=current_user_id)
        return render(request, self.template, {'posts': posts, 'debug': current_user_id})


def logout_view(request):
    logout(request)
    return redirect(request, '')

