"""
Url mapping for the comment API.
"""

from django.urls import path, include

from comments import views

app_name = 'comments'

urlpatterns = [
    path('',views.list_posts_view,name='list'),
    path('create/',views.create_comment_view,name='create'),
    path('<int:pk>/',views.manage_comment_view, name = 'manage'),
    path('myComments/',views.list_my_comments_view, name = 'myComments'),
    path('like/<int:pk>/',views.like_a_post_view, name = 'like'),
]