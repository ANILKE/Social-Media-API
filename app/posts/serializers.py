""""
Serializers for Posts.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from core.models import Post
from user.serializers import OwnerSerializer
from comments.serializers import CommentViewSerializer


class PostSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only= True)
    class Meta:
        model = Post
        fields = [
            'id',
            'owner',
            'content',
            'likes',
            ]
        read_only_fields = ['owner','likes']
        ordering_fields = ['id']

class PostDetailSerializer(PostSerializer):
    fields_to_be_removed = []
    liked_users = OwnerSerializer(read_only= True, many = True)
    comments = CommentViewSerializer(read_only= True, many = True)
    class Meta(PostSerializer.Meta):
        fields = PostSerializer.Meta.fields +[
            'comments',
            'liked_users'
        ]
        read_only_fields = ['id','comments','liked_users','likes','owner']
        # extra_kwargs = {
        #     'liked_users': {'write_only': True},
        #     'comments': {'write_only': True},
            
        # }
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in self.fields_to_be_removed:
            try:
                if rep[field] is None:  # checks if value is 'None', this is different from "emptiness"
                    rep.pop(field)
            except KeyError:
                pass
        return rep