from django.forms.models import model_to_dict

from apps.post.models import Post


def get_post_data(post_instance):
    post = model_to_dict(post_instance)
    post['likes'] = Post.get_number_of_likes(post_instance)
    post['creation_date'] = post_instance.creation_date
    return post
