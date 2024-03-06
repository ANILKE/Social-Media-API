""""
Serializers for Posts.
"""
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse

from core.models import Comment
from user.serializers import OwnerSerializer


class CommentSerializer(serializers.ModelSerializer):
    fields_to_be_removed = []
    owner = OwnerSerializer(read_only = True)
    liked_users = OwnerSerializer(read_only = True, many = True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'related_post_id',
            'owner',
            'content',
            'likes',
            'liked_users',
            ]
        read_only_fields = ['owner','likes','id','liked_users']
        ordering_fields = ['related_post_id']
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
        

class CommentViewSerializer(serializers.ModelSerializer):
    fields_to_be_removed = []
    owner = OwnerSerializer(read_only = True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'owner',
            'content',
            'likes',
            ]
        read_only_fields = ['owner','likes','id','liked_users']
        ordering_fields = ['related_post_id']