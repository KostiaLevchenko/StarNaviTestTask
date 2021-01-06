from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.analytics.services.analytics_service import AnalyticsService


class AnalyticsViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['GET'])
    def get_user_activity(self, request, *args, **kwargs):
        try:
            user_activity = AnalyticsService.get_user_activity(profile_id=self.request.query_params.get('id'))
            return Response(user_activity, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'])
    def get_likes_per_day(self, request, *args, **kwargs):
        try:
            likes_analytics = AnalyticsService.get_likes_per_day(
                date_from=self.request.query_params.get('date_from'), date_to=self.request.query_params.get('date_to')
            )
            return Response(likes_analytics, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
