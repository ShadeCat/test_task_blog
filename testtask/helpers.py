from testtask.models import User


def get_list_of_subscribers(username):
    subscribes_list = list(User.objects.get(username=username).subscribe.all())
    return [user.username for user in subscribes_list]


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
        user_object.subscribe.remove(author_object)
