from flask import Flask, request, jsonify
from atlas import AtlasClient
from os import environ as env
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
atlas_client = AtlasClient("mongodb+srv://ashleighwong0526:aMXUWlkcpZJnwJFb@finance0.ko1mg.mongodb.net/?retryWrites=true&w=majority&appName=finance0", "users")

@app.route('/')
def index():
    return jsonify({"message": "Welcome to the API. Available endpoints: /api/register, /api/user"}), 200

@app.route('/api/register', methods=['POST'])
def register_user():
    user_data = request.json
    
    # Here we don't need auth0_user_id since we don't require authentication
    users_collection = atlas_client.get_collection('info')
    existing_user = users_collection.find_one({'auth0_id': user_data.get('auth0_id')})

    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    new_user_id = atlas_client.insert_one('info', user_data)
    return jsonify({"message": "User registered successfully", "user_id": str(new_user_id)}), 201

@app.route('/api/user', methods=['GET'])
def get_user():
    # This endpoint now returns user data based on some identifier you might provide in the request
    user_id = request.args.get('auth0_id')  # Assume you're passing auth0_id in query params
    user = atlas_client.find('info', {'auth0_id': user_id}, limit=1)
    if user:
        return jsonify(user[0]), 200
    return jsonify({"message": "User not found"}), 404

@app.route('/api/user', methods=['PUT'])
def update_user():
    user_id = request.args.get('auth0_id')  # Again, assuming you're passing auth0_id in query params
    update_data = request.json
    result = atlas_client.update_one('info', {'auth0_id': user_id}, {'$set': update_data})
    if result:
        return jsonify({"message": "User updated successfully"}), 200
    return jsonify({"message": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)