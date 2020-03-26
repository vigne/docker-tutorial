import base64
import datetime
import os

from bson import json_util, ObjectId
from flask import json

from server import mongo, api  # api only needed for expire settings

# init database

def reset_database():
    # create collection, set indices
    mongo.db.tokens.drop()
    mongo.db.create_collection("tokens")
    mongo.db.tokens.create_index([("user", -1)])  # needs to be an array due to multifield support
    mongo.db.tokens.create_index("creation_date", expireAfterSeconds=api.config.get("TOKEN_EXP"))  # TTL index used for token expiration
    mongo.db.tokens.insert({"_id": "admin-unlimited", "user": "ralph", "creation_date": datetime.datetime.now() + datetime.timedelta(days=1000)})

    mongo.db.users.drop()
    mongo.db.create_collection("users")
    mongo.db.tokens.create_index([("follows", -1)])

    mongo.db.posts.drop()
    mongo.db.create_collection("posts")
    mongo.db.tokens.create_index([("author", -1)])
    # index overlaps 100% with the data needed by the query in get_posts_by_category
    mongo.db.tokens.create_index([("category", -1)])



# user management

def register_user(user_data):
    # new_user = mongo.db.users.insert_one(user_data)  # TODO: Python3
    new_user = mongo.db.users.insert(user_data)
    return new_user

def delete_user(user_id):
    mongo.db.users.delete_one({"_id": user_id})
    mongo.db.tokens.delete_one({"user": user_id})

def get_all_users():
    return json.loads(json_util.dumps(mongo.db.users.find({}, {"name": 1})))

def get_user(user_id):
    return json.loads(json_util.dumps(mongo.db.users.find_one_or_404({"_id": user_id})))

def get_user_name(user_id):
    return mongo.db.users.find_one_or_404({"_id": user_id}, {'_id': 0, "name": 1})['name']



# token managment

def get_user_token(user):
    token = json.loads(json_util.dumps(mongo.db.tokens.find_one({"user": user})))
    if token is None:
        token = {
            "user": user,
            "_id": base64.b64encode(os.urandom(24)).decode('utf-8'),  # settings it as ID allows to use the implicit index and ensures token uniquenes
            "creation_date": datetime.datetime.utcnow()  # having two dates is just for illustration of TTL
        }
        mongo.db.tokens.insert_one(token)
    return json.loads(json_util.dumps(token))

def verify_user_token(token):
    try:
        return mongo.db.tokens.find_one({"_id": token}, {"user": 1, "_id": 0})["user"]
    except TypeError:
        return None

def verify_user_password(username, password):
    return mongo.db.users.find_one({"_id": username, "password": password})

def get_featured_posts(limit=0):
    # projection pipline:
    # 1. sort to allow (2) limitation
    # 3. count comments on cropped array
    # return json.loads(json_util.dumps(mongo.db.posts.find({},{'comments': 0})))

    # 1. match and sort
    pipline = [{ "$sort": {"creation_date": -1}}]

    # 2. limit if possible
    if limit > 0:
        pipline.append({ "$limit": limit})

    # 2. count comments and project
    pipline.append({
            "$project": {
                "uri": "$uri",
                "author_name": "$author_name",
                "creation_date": "$creation_date",
                "category": "$category",
                "comment_count": { "$cond": { "if": { "$isArray": "$comments" }, "then": { "$size": "$comments" }, "else": "0"} }
            }
         })
    posts = mongo.db.posts.aggregate(pipline)
    return json.loads(json_util.dumps(posts))



# posts

def store_post(post):
    # application level consistency (no not null)
    if (not 'category' in post) or (post['category'] == ''):
        raise Exception("Missing 'category' attribute")
    return json.loads(json_util.dumps(mongo.db.posts.insert(post)))

def get_post(post_id):
    return json.loads(json_util.dumps(mongo.db.posts.find_one_or_404({"_id": ObjectId(post_id)})))

def add_comment(post_id, comment):
    # application level consistency
    if mongo.db.posts.find_one({'_id': ObjectId(post_id)}) is None:
        raise Exception("Missing post to comment on")

    mongo.db.posts.update(
        { "_id": ObjectId(post_id)},
        { "$push": {"comments": { "$each": [comment], "$position": 0}}}
    )



# queries

def get_user_activity(user_id):
    return json.loads(json_util.dumps(mongo.db.posts.find({
            "$or": [
                {"author": user_id},
                {"comments": {"$elemMatch": {"author": user_id}}},
            ]
        }
    ).sort("creation_date", -1)))

def get_posts_per_user(user_id):
    # supports pagination
    # pay attention how pipline saves resources

    # 1. match and sort
    pipline = [{"$match": {"author": user_id}}, { "$sort": {"creation_date": -1}}]

    # 2. count comments and project
    pipline.append({
            "$project": {
                "uri": "$uri",
                "username": "$author",
                "author_name": "$author_name",
                "creation_date": "$creation_date",
                "category": "$category",
                "comment_count": { "$cond": { "if": { "$isArray": "$comments" }, "then": { "$size": "$comments" }, "else": "0"} }
            }
         })

    posts = mongo.db.posts.aggregate(pipline)
    if posts is None:
        posts = []
    return json.loads(json_util.dumps(posts))


def get_comments_per_user(user_id):
    # supports pagination
    # pay attention how pipline saves resources

    # 1. match and sort
    pipline = [
        { "$match": {"comments": {"$elemMatch": {"author": user_id}}}},
        { "$sort": {"creation_date": -1}}]

    # 2. unwind (exploit) comments array
    # this is heavy on the server, but the price we have to pay for the embeded documents
    # so it's true what they say, there is no free lunch ;-)
    pipline.append(
        { "$unwind": "$comments"},
    )
    # 3. filter again for comment authored by userid
    pipline.append(
        { "$match": {"comments.author": user_id}},
    )

    # 4. project
    pipline.append({
            "$project": {
                "creation_date": "$comments.creation_date",
                "text": "$comments.text",
            }
         })

    posts = mongo.db.posts.aggregate(pipline)
    if posts is None:
        posts = []
    return json.loads(json_util.dumps(posts))

def get_posts_by_category(category_id, page=None, items_per_page=None):
    # supports pagination
    # pay attention how pipline saves resources

    # 1. match and sort
    pipline = [{"$match": {"category": category_id}}, { "$sort": {"creation_date": -1}}]


    # 2. reduce elements (pagination)
    page = 0 if page is None else int(page)
    if page > 0:
        items_per_page = 10 if items_per_page is None else items_per_page
        pipline.append({"$skip": int(page)*int(items_per_page)})
    items_per_page = None if items_per_page is None else int(items_per_page)
    if items_per_page is not None:
        pipline.append({"$limit": int(items_per_page)})

    # 3. count comments and project
    pipline.append({
            "$project": {
                "uri": "$uri",
                "author_name": "$author_name",
                "creation_date": "$creation_date",
                "category": "$category",
                "comment_count": { "$cond": { "if": { "$isArray": "$comments" }, "then": { "$size": "$comments" }, "else": "0"} }
            }
         })

    posts = mongo.db.posts.aggregate(pipline)
    return json.loads(json_util.dumps(posts))

def count_posts_by_category(category_id=None):
    # bucket counting
    return json.loads(json_util.dumps(mongo.db.posts.aggregate([{
            "$group": { "_id": "$category", "count": {"$sum" : 1}}
        }])))
