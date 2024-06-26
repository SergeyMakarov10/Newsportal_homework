from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from .resources import *
from django.urls import reverse
from django.core.cache import cache


class Author (models.Model):
    author_user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.author_user.username

    def update_rating(self):
        post_rating = self.post_set.all().aggregate(rating_sum=Sum('rating'))['rating_sum']
        user_rating = self.author_user.comment_set.all().aggregate(rating_sum=Sum('rating'))['rating_sum']
        comment_rating = \
            Comment.objects.filter(comment_post__author=self).aggregate(rating_sum=Sum('rating'))['rating_sum']

        self.author_rating = post_rating * 3 + user_rating + comment_rating
        self.save()


class Category (models.Model):
    category_name = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.category_name


class Post (models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    category_type = models.CharField(max_length=2, choices=post_type, default=article, verbose_name='Тип')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    post_category = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        text = self.text[:124]
        if len(self.text) > 124:
            text += '...'
        return text

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'post-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


class PostCategory (models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment (models.Model):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
