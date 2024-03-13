"""
Url mapping for the post API.
"""

from django.urls import path, include
from django.views.decorators.cache import cache_page

from posts import views

app_name = 'posts'

urlpatterns = [
    path('',cache_page(60)(views.list_posts_view),name='list'),
    path('create/',views.create_post_view,name='create'),
    path('<int:pk>/',views.manage_posts_view, name = 'manage'),
    path('myPosts/',cache_page(60)(views.list_my_posts_view), name = 'myPosts'),
    path('like/<int:pk>/',views.like_a_post_view, name = 'like'),
]