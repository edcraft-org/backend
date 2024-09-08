from flask import Blueprint, request, jsonify, current_app
from models.user import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    user = User(**data)
    user_id = current_app.mongo.db.users.insert_one(user.to_dict()).inserted_id
    return jsonify(str(user_id)), 201

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = current_app.mongo.db.users.find()
    users_list = []
    for user in users:
        user['_id'] = str(user['_id'])
        users_list.append(user)
    return jsonify(users_list), 200
