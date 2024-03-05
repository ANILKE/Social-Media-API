""""
Serializers for Friendships.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse

from core.models import Followship


class FriendshipSerializer(serializers.ModelSerializer):
    follower_profile = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Followship
        fields = [
            'follower',
            'follower_profile',
            ]
       
        
    def get_follower_profile(self, obj):
        request = self.context.get("request")
        if request is None:
            return None
        return  reverse("user:profile" ,kwargs={'pk': obj.follower.id},  request=request)

class FriendshipDetailSerializer(FriendshipSerializer):

    class Meta(FriendshipSerializer.Meta):
        fields = FriendshipSerializer.Meta.fields +[
            'id',
            'following',
            'since',
        ]
        read_only_fields = ['id','follower',]
        extra_kwargs = {
            'following': {'write_only': True},
        }