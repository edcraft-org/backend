from app import mongo

def get_user(user_id):
    return mongo.db.users.find_one({'_id': user_id})

def create_user(username, email, role):
    user_id = mongo.db.users.insert_one({
        'username': username,
        'email': email,
        'role': role
    }).inserted_id
    return user_id
