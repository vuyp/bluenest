from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for all routes
bcrypt = Bcrypt(app)

# In-memory data stores
users = []
posts = []
user_id_counter = 1
post_id_counter = 1

@app.route('/register', methods=['POST'])
def register():
    global user_id_counter
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'error': 'Missing username, email, or password'}), 400

    # Check for uniqueness
    if any(user['username'] == username for user in users):
        return jsonify({'error': 'Username already exists'}), 409
    if any(user['email'] == email for user in users):
        return jsonify({'error': 'Email already exists'}), 409

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    new_user = {
        'user_id': user_id_counter,
        'username': username,
        'email': email,
        'password_hash': hashed_password
    }
    users.append(new_user)
    user_id_counter += 1
    return jsonify({'message': 'User registered successfully', 'user': new_user}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Missing email or password'}), 400

    user = next((user for user in users if user['email'] == email), None)

    if user and bcrypt.check_password_hash(user['password_hash'], password):
        # In a real app, return a token (e.g., JWT)
        return jsonify({'message': 'Login successful', 'user_id': user['user_id']}), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401

@app.route('/posts', methods=['POST'])
def create_post():
    global post_id_counter
    data = request.get_json()
    user_id = data.get('user_id') 
    content = data.get('content')

    if not user_id or not content:
        return jsonify({'error': 'Missing user_id or content'}), 400

    # Check if user exists (optional, but good practice)
    if not any(user['user_id'] == user_id for user in users):
        return jsonify({'error': 'User not found'}), 404
        
    new_post = {
        'post_id': post_id_counter,
        'user_id': user_id,
        'content': content
    }
    posts.append(new_post)
    post_id_counter += 1
    return jsonify({'message': 'Post created successfully', 'post': new_post}), 201

@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts), 200

if __name__ == '__main__':
    app.run(debug=True)
