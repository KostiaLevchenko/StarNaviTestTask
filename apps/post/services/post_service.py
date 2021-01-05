from apps.post.models import Post
from apps.post.serializer import PostSerializer
from apps.post.utils.utils import get_post_data


class PostService:

    @staticmethod
    def get(post_id):
        post_instance = Post.objects.get(pk=post_id)
        return get_post_data(post_instance=post_instance)

    @staticmethod
    def create(post_data, profile):
        post_data['author'] = profile.get('profile').get('id')
        serializer = PostSerializer(data=post_data)
        serializer.is_valid(raise_exception=True)
        post_instance = serializer.create(validated_data=serializer.validated_data)
        return get_post_data(post_instance=post_instance)

    @staticmethod
    def like(post_id, profile):
        post_instance = Post.objects.get(pk=post_id)
        post_instance.likes.add(profile.get('profile').get('id'))
        return get_post_data(post_instance=post_instance)

    @staticmethod
    def unlike(post_id, profile):
        post_instance = Post.objects.get(pk=post_id)
        post_instance.likes.remove(profile.get('profile').get('id'))
        return get_post_data(post_instance=post_instance)
