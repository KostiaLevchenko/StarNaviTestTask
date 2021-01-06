from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

import datetime

from apps.user_profile.services.user_profile_service import UserProfileService


class UserActivityMiddleware(MiddlewareMixin):

    def respond(self, get_response):
        self.get_response = get_response

    def process_request(self, request):
        response = self.get_response(request)
        current_url = resolve(request.path_info).url_name
        if current_url != 'sign-up' and current_url != 'sign-in' and current_url != 'auth-confirm-activate':
            UserProfileService.update_user_last_activity(
                user=request.user.id,
                last_activity_date_time={'last_activity': datetime.datetime.now()}
            )
        return response
