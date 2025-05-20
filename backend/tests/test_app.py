import pytest
import json

# Assuming tests are run from the 'backend' directory (e.g., `cd backend; python -m pytest`)
# So, 'app.py' is in the current path.
from app import app as flask_app  # This is the Flask instance: app = Flask(__name__)
from app import users, posts      # These are the global lists: users = [], posts = []
import app as app_module          # This is the module app.py itself, to reset global counters

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    
    # Reset global in-memory stores and counters from app_module before each test
    users.clear()  # Direct modification of imported list 'users'
    posts.clear()  # Direct modification of imported list 'posts'
    
    # Counters are global variables in app.py. To reset them, we need to modify them in their module.
    app_module.user_id_counter = 1
    app_module.post_id_counter = 1
    
    with flask_app.test_client() as current_client:
        yield current_client
    
    # Optional: Cleanup after tests. Resetting at the start of the fixture is typical for pytest.
    # users.clear()
    # posts.clear()
    # app_module.user_id_counter = 1
    # app_module.post_id_counter = 1

# --- Test User Registration ---
def test_register_success(client):
    """Test successful user registration."""
    response = client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password123'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'User registered successfully'
    assert data['user']['username'] == 'testuser'
    assert data['user']['email'] == 'test@example.com'
    assert 'user_id' in data['user']
    assert data['user']['user_id'] == 1 # First user
    assert len(users) == 1
    assert users[0]['username'] == 'testuser'
    assert users[0]['user_id'] == 1
    assert app_module.user_id_counter == 2 # Counter should have incremented

def test_register_missing_data(client):
    """Test registration with missing email."""
    response = client.post('/register', json={
        'username': 'testuser2',
        'password': 'password123'
        # Email is missing
    })
    data = response.get_json()
    assert response.status_code == 400
    assert 'error' in data
    assert data['error'] == 'Missing username, email, or password'
    assert len(users) == 0
    assert app_module.user_id_counter == 1 # Counter should not have incremented

def test_register_duplicate_username(client):
    """Test registration with a duplicate username."""
    client.post('/register', json={'username': 'testuser', 'email': 'test1@example.com', 'password': 'password123'})
    
    response = client.post('/register', json={
        'username': 'testuser', # Duplicate username
        'email': 'test2@example.com',
        'password': 'password123'
    })
    data = response.get_json()
    assert response.status_code == 409
    assert data['error'] == 'Username already exists'
    assert len(users) == 1 # Only the first user should be registered
    assert app_module.user_id_counter == 2 # Counter incremented for the first user only

def test_register_duplicate_email(client):
    """Test registration with a duplicate email."""
    client.post('/register', json={'username': 'testuser1', 'email': 'test@example.com', 'password': 'password123'})
    
    response = client.post('/register', json={
        'username': 'testuser2',
        'email': 'test@example.com', # Duplicate email
        'password': 'password123'
    })
    data = response.get_json()
    assert response.status_code == 409
    assert data['error'] == 'Email already exists'
    assert len(users) == 1
    assert app_module.user_id_counter == 2

# --- Test User Login ---
def test_login_success(client):
    """Test successful user login."""
    reg_response = client.post('/register', json={'username': 'loginuser', 'email': 'login@example.com', 'password': 'password123'})
    assert reg_response.status_code == 201
    registered_user_id = reg_response.get_json()['user']['user_id']
    
    response = client.post('/login', json={
        'email': 'login@example.com',
        'password': 'password123'
    })
    data = response.get_json()
    assert response.status_code == 200
    assert data['message'] == 'Login successful'
    assert 'user_id' in data
    assert data['user_id'] == registered_user_id

def test_login_incorrect_password(client):
    """Test login with an incorrect password."""
    client.post('/register', json={'username': 'loginuser', 'email': 'login@example.com', 'password': 'password123'})
    
    response = client.post('/login', json={
        'email': 'login@example.com',
        'password': 'wrongpassword'
    })
    data = response.get_json()
    assert response.status_code == 401
    assert data['error'] == 'Invalid email or password'

def test_login_non_existent_user(client):
    """Test login with a non-existent email."""
    response = client.post('/login', json={
        'email': 'nouser@example.com',
        'password': 'password123'
    })
    data = response.get_json()
    assert response.status_code == 401 
    assert data['error'] == 'Invalid email or password'

# --- Test Posts ---
def test_create_post_success(client):
    """Test creating a post successfully."""
    reg_response = client.post('/register', json={'username': 'postuser', 'email': 'postuser@example.com', 'password': 'password'})
    user_id = reg_response.get_json()['user']['user_id']

    response = client.post('/posts', json={
        'user_id': user_id,
        'content': 'This is a test post.'
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data['message'] == 'Post created successfully'
    assert data['post']['content'] == 'This is a test post.'
    assert data['post']['user_id'] == user_id
    assert data['post']['post_id'] == 1 # First post
    assert len(posts) == 1
    assert posts[0]['content'] == 'This is a test post.'
    assert posts[0]['post_id'] == 1
    assert app_module.post_id_counter == 2 # Counter should have incremented

def test_create_post_missing_data(client):
    """Test creating a post with missing content or user_id."""
    reg_response = client.post('/register', json={'username': 'postuser', 'email': 'postuser@example.com', 'password': 'password'})
    user_id = reg_response.get_json()['user']['user_id']
    
    # Missing content
    response_no_content = client.post('/posts', json={'user_id': user_id})
    data_no_content = response_no_content.get_json()
    assert response_no_content.status_code == 400
    assert data_no_content['error'] == 'Missing user_id or content'
    
    # Missing user_id
    response_no_user = client.post('/posts', json={'content': 'A post without a user'})
    data_no_user = response_no_user.get_json()
    assert response_no_user.status_code == 400
    assert data_no_user['error'] == 'Missing user_id or content'
    
    assert len(posts) == 0
    assert app_module.post_id_counter == 1 # Counter should not increment

def test_create_post_user_not_found(client):
    """Test creating a post for a non-existent user."""
    response = client.post('/posts', json={
        'user_id': 999, # Assuming user_id 999 does not exist
        'content': 'This post should fail.'
    })
    data = response.get_json()
    assert response.status_code == 404 
    assert data['error'] == 'User not found'
    assert len(posts) == 0
    assert app_module.post_id_counter == 1

def test_get_posts_empty(client):
    """Test fetching posts when there are none."""
    response = client.get('/posts')
    data = response.get_json()
    assert response.status_code == 200
    assert isinstance(data, list)
    assert len(data) == 0

def test_get_posts_with_content(client):
    """Test fetching posts when some exist."""
    reg_response = client.post('/register', json={'username': 'postuser', 'email': 'postuser@example.com', 'password': 'password'})
    user_id = reg_response.get_json()['user']['user_id']
    
    client.post('/posts', json={'user_id': user_id, 'content': 'First post!'})
    client.post('/posts', json={'user_id': user_id, 'content': 'Second post!'})

    response = client.get('/posts')
    data = response.get_json()
    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]['content'] == 'First post!'
    assert data[0]['post_id'] == 1
    assert data[1]['content'] == 'Second post!'
    assert data[1]['post_id'] == 2
    assert app_module.post_id_counter == 3 # Incremented for each post
