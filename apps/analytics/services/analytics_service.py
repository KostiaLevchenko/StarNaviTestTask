from django.contrib.auth.models import User

from datetime import datetime
from apps.post.models import Like
from django.db.models import Count
from django.db.models.functions import TruncDay
from apps.user_profile.models import UserProfile


class AnalyticsService:
    @staticmethod
    def get_user_activity(profile_id):
        profile_instance = UserProfile.objects.get(pk=profile_id)
        user = User.objects.get(email=profile_instance.email)
        return {'last_login': user.last_login, 'last_activity': profile_instance.last_activity}

    @staticmethod
    def get_likes_per_day(date_from, date_to):
        likes = (
            Like.objects.filter(
                like_date__range=(datetime.strptime(date_from, '%Y-%m-%d'), datetime.strptime(date_to, '%Y-%m-%d'))
            )
            .annotate(day=TruncDay('like_date'))
            .values('day')
            .annotate(likes_per_day=Count('id'))
            .order_by()
        )
        return list(likes)
