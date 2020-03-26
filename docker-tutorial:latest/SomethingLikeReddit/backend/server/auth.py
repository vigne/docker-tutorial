from server import api

from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

import mongo_dao as db

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username, password):
    if db.verify_user_password(username, password) is None:
        return False
    g.current_user = username
    return True

@basic_auth.error_handler
def basic_auth_error():
    return ("Unauthorized", 401)

@token_auth.verify_token
def verify_token(token):
    g.current_user = db.verify_user_token(token) if token else None
    return g.current_user is not None

@token_auth.error_handler
def token_auth_error():
    return ("Unauthorized", 401)

@api.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    return jsonify(db.get_user_token(g.current_user))
