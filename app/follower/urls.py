"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from follower import views


router = DefaultRouter()
router.register('follower', views.FollowerViewSet,basename = 'follower')

app_name = 'followers'

urlpatterns = [
    path('',include(router.urls)),
]

