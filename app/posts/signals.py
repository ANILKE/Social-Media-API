from django.db.models.signals import pre_delete, post_delete, post_save
from core.models import Post
from django.dispatch import receiver
from app.celery import like_post1

from posts.tasks import like_post

import django 


@receiver (pre_delete, sender=Post)
def pre_delete_post(sender, **kwargs) :
    print(f"You are about to delete the post with id: {kwargs['instance'].id}!!!")


@receiver (post_delete, sender=Post)
def delete_post(sender, **kwargs) :
    print(f"You have just delete post id:{kwargs['instance'].id} and content: {kwargs['instance'].content}")


post_liked_signal = django.dispatch.Signal()
@receiver(post_save, sender=Post)
def post_liked(sender,  post_id=None, user_id=None, is_like=False, **kwargs):
    if(is_like):
        print("signal comes")
        like_post.apply_async(args=(post_id,user_id))

post_liked_signal.connect(post_liked)