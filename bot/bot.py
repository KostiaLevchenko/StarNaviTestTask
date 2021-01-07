import yaml
import json
import requests
from random import randrange, choice

HOST = 'http://localhost:8000'


def config_reader():
    with open('bot_config.yaml') as file:
        config_list = yaml.load(file, Loader=yaml.FullLoader)
    return config_list


def create_bots(number_of_users, max_posts_per_user):
    created_bots = []
    created_posts = []
    for user_index in range(number_of_users):
        requests.post(
            url=f'{HOST}/api/auth-confirm/create_user_with_bot/',
            data={
                "email": f"bot{user_index}@gmail.com",
                "username": f"bot{user_index}",
                "first_name": f"bot{user_index}",
                "last_name": f"bot{user_index}",
                "password": "password",
                "password2": "password"
            }
        )
        sign_in_response = requests.post(
            url=f'{HOST}/api/auth/sign-in/',
            data={
                "email": f"bot{user_index}@gmail.com",
                "password": "password"
            }
        )
        json_data = json.loads(sign_in_response.text)
        for post in range(randrange(1, max_posts_per_user)):
            create_post_response = requests.post(
                url=f'{HOST}/api/post/create_post/',
                data={
                    "title": "some title",
                    "body": "some text"
                },
                headers={'Authorization': f'TOKEN {json_data.get("token")}'}
            )

            create_post_response_data = json.loads(create_post_response.text)
            created_posts.append(create_post_response_data.get('id'))
        created_bots.append({'user': json_data.get('id'), 'token': json_data.get('token')})
    return {'created_bots': created_bots, 'created_posts': created_posts}


def make_likes(created_bots, max_likes_per_user, posts):
    likes = []
    for bot in created_bots:
        for like in range(randrange(1, max_likes_per_user)):
            like_response = requests.get(
                url=f'{HOST}/api/post/like/?id={choice(posts)}',
                headers={'Authorization': f'TOKEN {bot.get("token")}'}
            )
            like_response_data = json.loads(like_response.text)
            likes.append(like_response_data.get('id'))
    return likes


def main():
    data = config_reader()
    created_bots = create_bots(
        number_of_users=data.get('number_of_users'), max_posts_per_user=data.get('max_posts_per_user')
    )
    likes = make_likes(
        created_bots=created_bots.get('created_bots'),
        max_likes_per_user=data.get('max_likes_per_user'),
        posts=created_bots.get('created_posts')
    )
    report = {
        'number_of_created_users': len(created_bots.get('created_bots')),
        'number_of_created_posts': len(created_bots.get('created_posts')),
        'number_of_likes': len(likes)
    }
    print(report)


if __name__ == "__main__":
    main()
