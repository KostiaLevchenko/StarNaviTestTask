from django.forms.models import model_to_dict

from apps.post.serializer import PostSerializer
from apps.post.models import Post


class PostService:

    @staticmethod
    def create(post_data, profile):
        post_data['author'] = profile.get('profile').get('id')
        serializer = PostSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        post_instance = serializer.create(validated_data=serializer.validated_data)
        post = model_to_dict(post_instance)
        post['likes'] = Post.get_number_of_likes(post_instance)
        return post
