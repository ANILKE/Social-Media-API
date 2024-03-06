""""
Serializers for Posts.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'owner',
            ]
        read_only_fields = ['owner']
        ordering_fields = ['id']

class PostDetailSerializer(PostSerializer):
    fields_to_be_removed = []
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields +[
            'content',
            'likes',
            'comments',
            'liked_users'
        ]
        read_only_fields = ['id','likes','comments','owner','liked_users']
        extra_kwargs = {
            #'following': {'write_only': True},
        }
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in self.fields_to_be_removed:
            try:
                if rep[field] is None:  # checks if value is 'None', this is different from "emptiness"
                    rep.pop(field)
            except KeyError:
                pass
        return rep