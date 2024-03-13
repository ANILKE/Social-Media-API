from django.db.models.signals import pre_delete, post_delete
from core.models import Post
from django.dispatch import receiver

@receiver (pre_delete, sender=Post)
def pre_delete_post(sender, **kwargs) :
    print(f"You are about to delete the post with id: {kwargs['instance'].id}!!!")

@receiver (post_delete, sender=Post)
def delete_post(sender, **kwargs) :
    print(f"You have just delete post id:{kwargs['instance'].id} and content: {kwargs['instance'].content}")