from django.urls import path
from .views import *


urlpatterns = [
    path('news/', PostList.as_view(), name='news'),
    path('news/<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', PostUpdate.as_view(), name='news_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticleCreate.as_view(), name='article_create'),
    path('articles/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
]