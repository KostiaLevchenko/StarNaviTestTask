from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.http.response import HttpResponse

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from apps.user_profile.models import UserProfile
from apps.user_profile.serializer import UserProfileSerializer
from apps.user_profile.token_generator import account_activation_token
from apps.user_profile.utils import (
    obtain_token,
    create_user_token,
    update_profile_token,
    remove_internal_data_from_response,
    is_passwords_match,
    send_activation_email,
    get_image_url,
    CurrentUserOrSafeMethod
)


class RegistrationView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            is_passwords_match(password=data.get('password'), password2=data.get('password2'))
            serializer = UserProfileSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            profile_instance = serializer.create(serializer.validated_data)
            user = create_user_token(email=data.get('email'), password=data.get('password'))
            profile = update_profile_token(profile=profile_instance, user=user)
            profile = model_to_dict(profile)
            profile['avatar'] = get_image_url(image_path=profile.get('avatar'))
            obtain_token(user=user, profile=profile)
            remove_internal_data_from_response(data=profile)
            send_activation_email(user=user)
            return Response(profile, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthConfirm(viewsets.ModelViewSet):
    permission_classes = [CurrentUserOrSafeMethod]

    @action(detail=False, methods=['GET'])
    def activate(self, request, *args, **kwargs):
        try:
            uid_b64 = request.GET['uid']
            token_b64 = request.GET['token']
            uid = force_text(urlsafe_base64_decode(uid_b64))
            token = force_text(urlsafe_base64_decode(token_b64))
            user = User.objects.get(pk=uid)
            if user is not None and account_activation_token.check_token(user, token):
                user.is_active = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return HttpResponse('Thank you for your email confirmation. Now you can log into your account.')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            user = User.objects.get(email=data.get('email'))
            if not data.get('username'):
                data['username'] = data.get('email')
            if not user:
                raise Exception('User does not exist')
            elif not user.is_active:
                raise Exception('User is not yet activated')
            serializer = self.serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                profile_instance = UserProfile.objects.get(email=data.get('email'))
                profile = {'id': profile_instance.id, 'username': profile_instance.username}
                obtain_token(user=user, profile=profile)
                return Response(profile, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
