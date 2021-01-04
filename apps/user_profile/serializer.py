from rest_framework import serializers

from apps.user_profile.models import UserProfile
from apps.user_profile.utils.std_image_field import StdImageField


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = StdImageField(required=False, allow_null=True)

    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'first_name', 'last_name', 'avatar', 'user')

    def create(self, validated_data):
        user_profile = UserProfile.objects.create(**validated_data)
        return user_profile

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance
