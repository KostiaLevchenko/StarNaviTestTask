from django.contrib.auth.models import User

from apps.user_profile.models import UserProfile
from apps.user_profile.serializer import UserProfileSerializer
from apps.user_profile.utils.utils import (
    create_user,
    connect_user_to_profile,
    is_passwords_match,
    get_profile_data,
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
        serializer = UserProfileSerializer(data=profile_data)
        serializer.is_valid(raise_exception=True)
        profile_instance = serializer.create(serializer.validated_data)
        user = create_user(email=profile_data.get('email'), password=profile_data.get('password'))
        profile = connect_user_to_profile(profile=profile_instance, user=user)
        profile = get_profile_data(profile_instance=profile)
        return {'profile': profile, 'user': user}

    @staticmethod
    def get_user_activity(profile_id):
        profile_instance = UserProfile.objects.get(pk=profile_id)
        user = User.objects.get(email=profile_instance.email)
        return {'last_login': user.last_login}
