from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Category


class PostList(ListView):
    model = Post
    template_name = "post_list.html"
    ordering = '-creation_date'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = 'post'
