from django.forms.models import model_to_dict
from django.contrib.auth import get_user_model


from StarNaviTestTask.utils import get_image_url
from apps.user_profile.serializer import UserProfileSerializer


def create_user(email, password):
    user = get_user_model().objects.create(username=email, email=email, is_active=False)
    user.set_password(password)
    user.save()
    return user


def connect_user_to_profile(profile, user):
    user_update_data = {'id': profile.id, 'user': user.id}
    update_user = UserProfileSerializer(data=user_update_data, partial=True)
    update_user.is_valid(raise_exception=True)
    profile = update_user.update(profile, update_user.validated_data)
    return profile


def is_passwords_match(password, password2):
    if password != password2:
        raise Exception('Passwords do not match')
    else:
        return True


def get_profile_data(profile_instance):
    profile = model_to_dict(profile_instance)
    profile['avatar'] = get_image_url(image_path=profile.get('avatar'))
    del profile['password']
    del profile['user']
    return profile


def create_user_for_bot(email, password):
    user = get_user_model().objects.create(username=email, email=email, is_active=True)
    user.set_password(password)
    user.save()
    return user
