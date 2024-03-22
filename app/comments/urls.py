"""
Url mapping for the comment API.
"""

from django.urls import path, include
from django.views.decorators.cache import cache_page
#from app.decorators import custom_cache_page

from comments import views

app_name = 'comments'

urlpatterns = [
    path('',cache_page(60,key_prefix='')(views.list_posts_view),name='list'),
    path('create/',views.create_comment_view,name='create'),
    path('<int:pk>/',views.manage_comment_view, name = 'manage'),
    path('myComments/',cache_page(60,key_prefix='')(views.list_my_comments_view), name = 'myComments'),
    path('like/<int:pk>/',views.like_a_comment_view, name = 'like'),
]