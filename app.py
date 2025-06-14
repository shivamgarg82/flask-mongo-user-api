from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from bson.errors import InvalidId
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/user_db')

mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# Helper function to validate ObjectId
def validate_object_id(id_str):
    try:
        return ObjectId(id_str)
    except (InvalidId, TypeError):
        return None

# Helper function to format user response
def format_user(user):
    if user:
        user['_id'] = str(user['_id'])
        user.pop('password', None)  # Remove password from response
        return user
    return None

@app.route('/users', methods=['GET'])
def get_users():
    users = list(mongo.db.users.find())
    formatted_users = [format_user(user) for user in users]
    return jsonify(formatted_users)

@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    obj_id = validate_object_id(user_id)
    if not obj_id:
        return jsonify({"error": "Invalid user ID"}), 400
    
    user = mongo.db.users.find_one({"_id": obj_id})
    formatted_user = format_user(user)
    
    if formatted_user:
        return jsonify(formatted_user)
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Basic validation
    if not all(key in data for key in ['name', 'email', 'password']):
        return jsonify({"error": "Missing required fields"}), 400
    
    # Check if email already exists
    if mongo.db.users.find_one({"email": data['email']}):
        return jsonify({"error": "Email already exists"}), 400
    
    # Hash password
    hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    # Insert new user
    user_data = {
        "name": data['name'],
        "email": data['email'],
        "password": hashed_pw
    }
    
    result = mongo.db.users.insert_one(user_data)
    return jsonify({
        "message": "User created successfully",
        "id": str(result.inserted_id)
    }), 201

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    obj_id = validate_object_id(user_id)
    if not obj_id:
        return jsonify({"error": "Invalid user ID"}), 400
    
    data = request.get_json()
    updates = {}
    
    if 'name' in data:
        updates['name'] = data['name']
    if 'email' in data:
        updates['email'] = data['email']
    if 'password' in data:
        updates['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    
    result = mongo.db.users.update_one(
        {"_id": obj_id},
        {"$set": updates}
    )
    
    if result.modified_count:
        return jsonify({"message": "User updated successfully"})
    return jsonify({"error": "User not found or no changes made"}), 404

@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    obj_id = validate_object_id(user_id)
    if not obj_id:
        return jsonify({"error": "Invalid user ID"}), 400
    
    result = mongo.db.users.delete_one({"_id": obj_id})
    
    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"error": "User not found"}), 404

@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    # FIXME: This doesn't check if email already exists for another user
    # (I ran out of time but will fix in v2)
    updates = request.get_json()
    ...

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)