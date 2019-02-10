from testtask.models import User, Post
from django.core.mail import send_mail
import settings
from django.urls import reverse
from django.db.models import signals

def get_list_of_subscribers(username):
    subscribes_list = list(User.objects.get(username=username).subscribe.all())
    return [user.username for user in subscribes_list]


def get_list_of_read(username):
    read_list = list(User.objects.get(username=username).read.all())
    return [post.title for post in read_list]


def delete_read_marks(username, author):
    user = User.objects.get(username=username)
    read_posts = user.read.all()
    read_authors_posts = read_posts.filter(author=author)
    for post in read_authors_posts:
        user.read.remove(post)


def subscribe_or_unsubscribe(request):
    """Принимает POST запрос от формы с полями 'subscribe',
     'unsubscribe' с именем пользователя"""
    subscribe_author = request.POST.get('subscribe', None)
    unsubscribe_author = request.POST.get('unsubscribe', None)
    user = str(request.user)
    user_object = User.objects.get(username=user)
    if subscribe_author is not None:
        author_object = User.objects.get(username=subscribe_author)
        user_object.subscribe.add(author_object)
    elif unsubscribe_author is not None:
        author_object = User.objects.get(username=unsubscribe_author)
        delete_read_marks(user, author_object)
        user_object.subscribe.remove(author_object)


def send_email_to_subscribers(sender, instance, signal, *args, **kwargs):
    author = instance.author
    addressees = User.objects.filter(subscribe=author)
    for addressee in addressees:
        send_mail(
            'Новый пост!',
            'Пользователь ' + str(author) +
            'опубликовал новый пост. Вы можете увидеть его в своей ленте' +
            settings.DEFAULT_DOMAIN + str((reverse('private_blog', kwargs={'author': author}))),
            settings.EMAIL_HOST_USER,
            [addressee.email],
            fail_silently=False,
            )


signals.post_save.connect(send_email_to_subscribers, sender=Post)
