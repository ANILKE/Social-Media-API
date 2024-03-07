""""
Serializers for Friendships.
"""

from rest_framework import serializers
from rest_framework.reverse import reverse
from user.serializers import OwnerSerializer
from core.models import Followship


class FriendshipSerializer(serializers.ModelSerializer):
    follower = OwnerSerializer(read_only= True)
    class Meta:
        model = Followship
        fields = [
            'id',
            'follower',
            ]
       

class FriendshipDetailSerializer(FriendshipSerializer):
    fields_to_be_removed = ['follower_profile']
    follower_profile = serializers.SerializerMethodField(read_only = True)
    following = OwnerSerializer()
    class Meta(FriendshipSerializer.Meta):
        fields = FriendshipSerializer.Meta.fields +[
            'following',
            'since',
            'follower_profile',
        ]
        read_only_fields = ['id','follower',]
        extra_kwargs = {
            #'following': {'write_only': True},
        }
    def get_follower_profile(self, obj):
        request = self.context.get("request")
        if request is None:
            return None
        return  reverse("user:profile" ,kwargs={'pk': obj.follower.id},  request=request)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        for field in self.fields_to_be_removed:
            try:
                if rep[field] is None:  # checks if value is 'None', this is different from "emptiness"
                    rep.pop(field)
            except KeyError:
                pass
        return rep