from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response


from apps.post.services.post_service import PostService
from apps.user_profile.services.user_profile_service import UserProfileService


class PostViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['POST'])
    def create_post(self, request, *args, **kwargs):
        try:
            profile = UserProfileService.get(profile_data={'email': request.user})
            post = PostService.create(post_data=request.data, profile=profile)
            return Response(post, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'])
    def get_post(self, request, *args, **kwargs):
        try:
            post = PostService.get(post_id=self.request.query_params.get('id'))
            return Response(post, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['GET'])
    def like(self, request, *args, **kwargs):
        try:
            profile = UserProfileService.get(profile_data={'email': request.user})
            like = PostService.like(post_id=self.request.query_params.get('id'), profile=profile)
            return Response(like, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
