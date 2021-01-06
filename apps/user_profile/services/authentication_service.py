from django.contrib.auth import login
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from knox.models import AuthToken

from apps.user_profile.utils.token_generator import account_activation_token


class AuthenticationService:
    @staticmethod
    def obtain_token(user, profile):
        token, key = AuthToken.objects.create(user=user)
        data = {'token': key, 'pk': user.pk, 'success': True}
        profile['token'] = data.get('token')
        profile['success'] = data.get('success')
        return profile

    @staticmethod
    def activate_profile(request, uid_b64, token_b64):
        uid = force_text(urlsafe_base64_decode(uid_b64))
        token = force_text(urlsafe_base64_decode(token_b64))
        user = User.objects.get(pk=uid)
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return 'Thank you for your email confirmation. Now you can log into your profile.'
