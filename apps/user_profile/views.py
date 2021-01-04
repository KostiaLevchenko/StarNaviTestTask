from django.http.response import HttpResponse

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken

from apps.user_profile.utils.current_user import CurrentUserOrSafeMethod
from apps.user_profile.services.user_profile_service import UserProfileService
from apps.user_profile.services.authentication_service import AuthenticationService
from apps.user_profile.services.email_sending_service import EmailSendingService


class RegistrationView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            profile = UserProfileService.create(profile_data=data)
            AuthenticationService.obtain_token(user=profile.get('user'), profile=profile.get('profile'))
            EmailSendingService.send_profile_activation_email(user=profile.get('user'))
            return Response(profile.get('profile'), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AuthConfirm(viewsets.ModelViewSet):
    permission_classes = [CurrentUserOrSafeMethod]

    @action(detail=False, methods=['GET'])
    def activate(self, request, *args, **kwargs):
        try:
            uid_b64 = request.GET['uid']
            token_b64 = request.GET['token']
            profile = AuthenticationService.activate_profile(request=request, uid_b64=uid_b64, token_b64=token_b64)
            return HttpResponse(profile)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data.copy()
            profile = UserProfileService.get(profile_data=data)
            AuthenticationService.obtain_token(user=profile.get('user'), profile=profile.get('profile'))
            return Response(profile.get('profile'), status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
