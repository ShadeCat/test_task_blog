from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from testtask.models import *
from django.contrib.auth import logout
from testtask.forms import NewPost
from django.http import HttpResponseRedirect
from testtask.helpers import get_list_of_subscribers, get_list_of_read, subscribe_or_unsubscribe


class IndexView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'testtask/news.html'


class AuthorsView(View):
    template = 'testtask/authors.html'

    def get(self, request):
        authors = User.objects.all()
        return render(request, self.template, {'authors': authors, 'subscribes': get_list_of_subscribers(request.user)})

    def post(self, request):
        subscribe_or_unsubscribe(request)
        return HttpResponseRedirect('/authors/')


class MyBlogView(View):
    template = 'testtask/personal_blog.html'

    def get(self, request, author):
        current_user_id = User.objects.get(username=author).id
        posts = Post.objects.filter(author=current_user_id)
        return render(request, self.template, {'posts': posts, 'author': author})


class LentaView(View):
    template = 'testtask/lenta.html'

    def get(self, request):
        user = request.user.get_username()
        subscribes = User.objects.get(username=user).subscribe.all()
        subscribed_post = Post.objects.none()
        for subscribe in subscribes:
            subscribed_post |= Post.objects.filter(author=subscribe.pk)
        return render(request, self.template, {'posts': subscribed_post, 'read': get_list_of_read(user)})

    def post(self, request):
        readed_post_pk = request.POST.get('read', None)
        user = str(request.user)
        user_object = User.objects.get(username=user)
        author_object = Post.objects.get(pk=readed_post_pk)
        user_object.read.add(author_object)
        return HttpResponseRedirect('/lenta/')


class BlogWriteView(View):

    def post(self, request):
        author = request.user.get_username()
        author_id = User.objects.get(username=author).id
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
    return render(request, 'testtask/newpost.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(request, '')
