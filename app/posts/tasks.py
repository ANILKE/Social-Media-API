from __future__ import absolute_import, unicode_literals

from celery import shared_task

from django.core.cache import cache
from django.contrib.auth import get_user_model

from core.models import Post

@shared_task
def like_post(post_id, request_user_id):
    try:
        post = Post.objects.all().filter(pk=post_id).first()
        user = get_user_model().objects.all().filter(pk=request_user_id).first()
        post.likes += 1
        post.liked_users.add(user.id)
        post.save()
        cache.delete(f'post_{post.pk}')
        print('liked')
        return 0
    except Exception as e:
        print(f'Error: {e}')
        return 1
