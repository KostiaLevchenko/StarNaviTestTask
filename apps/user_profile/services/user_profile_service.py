from django.contrib.auth.models import User

from datetime import datetime

from apps.user_profile.models import UserProfile
from apps.user_profile.serializer import UserProfileSerializer
from apps.user_profile.utils.utils import (
    create_user,
    connect_user_to_profile,
    is_passwords_match,
    get_profile_data,
    create_user_for_bot,
)


class UserProfileService:
    @staticmethod
    def get(profile_data):
        user = User.objects.get(email=profile_data.get('email'))
        if not profile_data.get('username'):
            profile_data['username'] = profile_data.get('email')
        if not user:
            raise Exception('User does not exist')
        elif not user.is_active:
            raise Exception('User is not yet activated')
        profile_instance = UserProfile.objects.get(email=profile_data.get('email'))
        profile = get_profile_data(profile_instance=profile_instance)
        return {'profile': profile, 'user': user}

    @staticmethod
    def create(profile_data):
        is_passwords_match(password=profile_data.get('password'), password2=profile_data.get('password2'))
        profile_data['last_activity'] = datetime.now()
        serializer = UserProfileSerializer(data=profile_data)
        serializer.is_valid(raise_exception=True)
        profile_instance = serializer.create(validated_data=serializer.validated_data)
        user = create_user(email=profile_data.get('email'), password=profile_data.get('password'))
        profile = connect_user_to_profile(profile=profile_instance, user=user)
        profile = get_profile_data(profile_instance=profile)
        return {'profile': profile, 'user': user}

    @staticmethod
    def update_user_last_activity(user, last_activity_date_time):
        profile_instance = UserProfile.objects.get(user=user)
        serializer = UserProfileSerializer(data=last_activity_date_time, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_profile_instance = serializer.update_last_activity(
            instance=profile_instance, validated_data=serializer.validated_data
        )
        return get_profile_data(profile_instance=updated_profile_instance)

    @staticmethod
    def create_user_with_bot(profile_data):
        profile_data['last_activity'] = datetime.now()
        serializer = UserProfileSerializer(data=profile_data)
        serializer.is_valid(raise_exception=True)
        profile_instance = serializer.create(validated_data=serializer.validated_data)
        user = create_user_for_bot(email=profile_data.get('email'), password=profile_data.get('password'))
        profile = connect_user_to_profile(profile=profile_instance, user=user)
        profile = get_profile_data(profile_instance=profile)
        return {'profile': profile, 'user': user}
