import random
import requests
import traceback

import mongo_dao as db

from server import api

from datetime import datetime
from faker import Faker
from faker.providers import date_time, internet, lorem, profile
from flask import jsonify, abort, request, make_response
from requests.auth import HTTPBasicAuth
from faker.providers import BaseProvider


# create new provider class. Note that the class name _must_ be ``Provider``.
class Provider(BaseProvider):
    def category(self):
        categories = [
            "science",
            "sports",
            "news",
            "comedy"
        ]
        return self.random_element(categories)

@api.route('/init_db', methods=['POST'])
def init():
    print(request.args)
    number_of_user = request.args.get('users', 10, int)
    number_of_posts = request.args.get('posts', 100, int)
    number_of_comments = request.args.get('comments', 100, int)
    db.reset_database()

    # fill user
    fake = Faker()
    fake.add_provider(Provider)


    # create fake users
    users = [{
        "_id": fake.user_name(),
        "name": fake.name(),
        "address": fake.address(),
        "password": "changemenow",
        "mail": fake.free_email(),
        "follows": [fake.category() for __ in range(random.randint(0,2))]
        } for _ in range(number_of_user)]
    # add one account with known mail and pwd for demo
    for user in users:
        requests.post("http://localhost:5005/users", json=user)
    requests.post("http://localhost:5005/users", json={
        "_id": "ralph",
        "name": "Ralph Vigne",
        "address": fake.address(),
        "password": "pwd",
        "mail": "ralph@imse",
        "follows": ["science", "sports"]
        })


    # request access token
    headers = {
        'Authorization': "Bearer %s" % requests.post("http://localhost:5005/tokens", auth=HTTPBasicAuth('ralph', 'pwd')).json()["_id"]
    }

    # check if authorization worked
    profile = requests.get("http://localhost:5005/users/ralph", headers=headers)
    print(profile.json())

    # fill posts
    print(number_of_posts)
    posts = [{
        "uri": fake.uri(),
        "creation_date": fake.date_time_between(start_date="-30d", end_date="now", tzinfo=None),
        "category": fake.category(),
        "author": random.choice(users)["_id"],
        "author_name": fake.name(),  # for the test data we accept the inconsistency with names
        "comments": []
        } for _ in range(number_of_posts)]


    for post in posts:
        db.store_post(post)  # using this instead of REST allow for easy user switching and fake dates

    # inserting one post using REST
    requests.post('http://localhost:5005/posts', json={
        "uri": fake.uri(),
        "category": fake.category()
    }, headers=headers)

    # comments

    featured_posts = requests.get("http://localhost:5005/posts", headers=headers).json()
    for _ in range(number_of_comments):
        # create comment
        comment = {
            "author": random.choice(users)['_id'],
            "author_name": fake.name(),
            "text": fake.sentence(nb_words=20,
                                variable_nb_words=True,
                                ext_word_list=None),
            "creation_date": fake.date_time_between(
                        start_date=next(iter(post['comments']), post)["creation_date"],
                        end_date="now",
                        tzinfo=None),
        }
        post_id = random.choice(featured_posts)['_id']['$oid']
        try:
            db.add_comment(post_id, comment)
        except (Exception) as e:
            traceback.print_exc()
            abort(make_response(({"error": "Failed inserting comments", "exception": str(e)}, 500)))

    return ('Done inserting', 201)
