from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from testtask.models import *
from django.contrib.auth import logout
from testtask.forms import NewPost
from django.http import HttpResponseRedirect


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
    template = 'testtask/personal_blog.html'

    def get(self, request, author):
        current_user_id = User.objects.filter(username=author)[0].id
        posts = Post.objects.filter(author=current_user_id)
        return render(request, self.template, {'posts': posts, 'debug': current_user_id})


class BlogWriteView(View):

    def post(self, request):
        author = request.user.get_username()
        author_id = User.objects.filter(username=author)[0].id
        form = NewPost(request.POST)
        if form.is_valid():
            Post.objects.create(title=form.title, body=form.body, author=author_id)
            return HttpResponseRedirect('/save/')
        else:
            pass
        return redirect(request, '/')


def post_new(request):
    if request.method == 'POST':
        form = NewPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect('/')
    else:
        form = NewPost()
    return render(request, 'newpost.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(request, '')

