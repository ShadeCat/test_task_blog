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


class AuthorsView(View):
    template = 'testtask/authors.html'

    def get(self, request):
        current_user = request.user
        authors = User.objects.all()
        current_users_subscribes = list(User.objects.get(username=current_user).subscribe.all())
        current_users_subscribes = [user.username for user in current_users_subscribes]
        return render(request, self.template, {'authors': authors, 'subscribes': current_users_subscribes})

    def post(self, request):
        subscribe_author = request.POST.get('subscribe', None)
        unsubscribe_author = request.POST.get('unsubscribe', None)
        user = str(request.user)
        user_object = User.objects.get(username=user)
        if subscribe_author is not None:
            author_object = User.objects.get(username=subscribe_author)
            user_object.subscribe.add(author_object)
        elif unsubscribe_author is not None:
            author_object = User.objects.get(username=unsubscribe_author)
            user_object.subscribe.remove(author_object)
        return HttpResponseRedirect('/authors/')


class MyBlogView(View):
    template = 'testtask/personal_blog.html'

    def get(self, request, author):
        current_user_id = User.objects.get(username=author)[0].id
        posts = Post.objects.filter(author=current_user_id)
        return render(request, self.template, {'posts': posts, 'author': author})


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

