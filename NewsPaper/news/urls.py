from django.urls import path
from .views import *


urlpatterns = [
    path('', PostList.as_view(), name='news'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
]