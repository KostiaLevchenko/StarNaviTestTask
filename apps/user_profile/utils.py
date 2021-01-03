from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from knox.models import AuthToken

from rest_framework import permissions

from apps.user_profile.models import UserProfile
from apps.user_profile.serializer import UserProfileSerializer
from apps.user_profile.token_generator import account_activation_token


def obtain_token(user, profile):
    token, key = AuthToken.objects.create(user=user)
    data = {'token': key, 'pk': user.pk, 'success': True}
    profile['token'] = data.get('token')
    profile['success'] = data.get('success')
    return profile


def create_user_token(email, password):
    user = get_user_model().objects.create(username=email, email=email, is_active=False)
    user.set_password(password)
    user.save()
    return user


def update_profile_token(profile, user):
    user_update_data = {'id': profile.id, 'user': user.id}
    update_user = UserProfileSerializer(data=user_update_data, partial=True)
    update_user.is_valid(raise_exception=True)
    profile = update_user.update(profile, update_user.validated_data)
    return profile


def remove_internal_data_from_response(data):
    del data['password']
    del data['last_login']
    del data['user']


def is_passwords_match(password, password2):
    if password != password2:
        raise Exception('Passwords do not match')
    else:
        return True


def send_activation_email(user):
    profile_instance = UserProfile.objects.get(email=user)
    recipient_list = [user.email]
    send_email_from_template(
        subject="Activate your profile",
        template='activate_profile_email.html',
        recipient_list=recipient_list,
        template_variables={
            'username': profile_instance.username,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': urlsafe_base64_encode(force_bytes(account_activation_token.make_token(user))),
        }
    )


def send_email_from_template(subject="", recipient_list=None, template="", template_variables=None):
    if template_variables is None:
        template_variables = {}
    template_variables['site_url'] = f'{settings.NETWORK_PROTOCOL}://{settings.DOMAIN}/'
    from_email = settings.EMAIL_ADDRESS
    message = render_to_string(template, template_variables)
    send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=message)


def get_image_url(image_path):
    if image_path:
        return f'{settings.NETWORK_PROTOCOL}://{settings.DOMAIN}/media/{image_path}'
    else:
        return None


class CurrentUserOrSafeMethod(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and obj == request.user
