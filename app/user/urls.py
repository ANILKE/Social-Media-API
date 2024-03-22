"""
Url mapping for the user API.
"""

from django.urls import path, include
from django.views.decorators.cache import cache_page
#from app.decorators import custom_cache_page

from user import views

app_name = 'user'

urlpatterns = [
    path('create/',views.CreateUserView.as_view(),name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/',(views.ManageUserView.as_view()), name='me'),
    path('<int:pk>/',(views.ShowProfileView.as_view()),name='profile'),
    path('',include('follower.urls'),name = 'friends'),
]