from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.user_profile.models import UserProfile
from StarNaviTestTask.utils import send_email_from_template
from apps.user_profile.utils.token_generator import account_activation_token


class EmailSendingService:

    @staticmethod
    def send_profile_activation_email(user):
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
