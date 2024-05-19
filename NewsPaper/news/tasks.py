import datetime
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import Post, Category
from .signals import notify_about_new_post


@shared_task
def new_post_celery(pk):
    post = Post.objects.get(pk=pk)
    categories = post.post_category.all()
    title = post.title
    preview = post.preview()
    subscribers_emails = []
    for category in categories:
        subscribers = category.subscribers.all()
        for subscriber in subscribers:
            if subscriber.email not in subscribers_emails:
                subscribers_emails.append(subscriber.email)

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview[:50],
            'link': f'{settings.SITE_URL}/news/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails,
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_post():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(creation_date__gte=last_week)
    # set для получения списка уникальных значений
    categories = set(posts.values_list('post_category__category_name', flat=True))
    subscribers = set(Category.objects.filter(category_name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'weekly_post.html',
        {
            'link': f'http://127.0.0.1:8000',
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email='serjmak1010@yandex.ru',
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()
