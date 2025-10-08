import pytest
from app import app, load_history, save_submission, HISTORY_FILE, USERS_FILE, save_users
import os
import json
from datetime import datetime
from werkzeug.security import generate_password_hash

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    with app.test_client() as client:
        yield client

@pytest.fixture
def clean_history():
    """Clean up history file before and after test"""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    yield
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

@pytest.fixture
def clean_users():
    """Clean up users file before and after test"""
    if os.path.exists(USERS_FILE):
        os.remove(USERS_FILE)
    yield
    if os.path.exists(USERS_FILE):
        os.remove(USERS_FILE)

@pytest.fixture
def authenticated_client(client, clean_users):
    """Create a test user and login"""
    # Create a test user
    users = {
        '1': {
            'username': 'testuser',
            'password': generate_password_hash('testpass')
        }
    }
    save_users(users)
    
    # Login
    client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    })
    
    yield client

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Copilot Demo" in response.data

def test_form_submission_requires_login(client, clean_history):
    """Test that form submission requires authentication"""
    response = client.post("/", data={"name": "Alice"}, follow_redirects=False)
    assert response.status_code == 302  # Redirect to login

def test_form_submission_authenticated(authenticated_client, clean_history):
    """Test form submission when authenticated"""
    response = authenticated_client.post("/", data={"name": "Alice"})
    assert response.status_code == 200
    assert b"Alice" in response.data
    assert b"Your submission has been logged" in response.data

def test_history_page_requires_login(client, clean_history):
    """Test that history page requires authentication"""
    response = client.get('/history', follow_redirects=False)
    assert response.status_code == 302  # Redirect to login

def test_history_page_empty_authenticated(authenticated_client, clean_history):
    """Test history page when no submissions exist (authenticated)"""
    response = authenticated_client.get('/history')
    assert response.status_code == 200
    assert b'No submissions yet' in response.data

def test_history_page_with_submissions(authenticated_client, clean_history):
    """Test history page with submissions"""
    # First make a submission
    authenticated_client.post('/', data={'name': 'Test User'})
    
    # Check history page
    response = authenticated_client.get('/history')
    assert response.status_code == 200
    assert b'Test User' in response.data
    assert b'Total Submissions' in response.data

def test_clear_history(authenticated_client, clean_history):
    """Test clearing submission history"""
    # Make a submission first
    authenticated_client.post('/', data={'name': 'Test User'})
    
    # Clear history
    response = authenticated_client.post('/clear-history')
    assert response.status_code == 302  # Redirect response
    
    # Check that history is empty
    response = authenticated_client.get('/history')
    assert b'No submissions yet' in response.data

def test_save_submission_function(clean_history):
    """Test the save_submission function directly"""
    save_submission('Test User')
    
    # Check that file was created and contains the submission
    assert os.path.exists(HISTORY_FILE)
    
    history = load_history()
    assert len(history) == 1
    assert history[0]['name'] == 'Test User'
    assert 'timestamp' in history[0]
    assert 'formatted_time' in history[0]

def test_load_history_function(clean_history):
    """Test the load_history function"""
    # Test with no file
    history = load_history()
    assert history == []
    
    # Test with file
    save_submission('User 1')
    save_submission('User 2')
    
    history = load_history()
    assert len(history) == 2
    assert history[0]['name'] == 'User 1'
    assert history[1]['name'] == 'User 2'

def test_logging_file_creation(authenticated_client, clean_history):
    """Test that submissions create log entries"""
    # Clean up old log entries first
    if os.path.exists('submissions.log'):
        # Read existing content
        with open('submissions.log', 'r') as f:
            old_content = f.read()
    
    # Make a submission
    authenticated_client.post('/', data={'name': 'Log Test User'})
    
    # Check that log file exists (submissions.log)
    assert os.path.exists('submissions.log')
    
    # Read log file and check for entry
    with open('submissions.log', 'r') as f:
        log_content = f.read()
        assert 'Log Test User' in log_content
        assert 'New submission' in log_content

def test_user_registration(client, clean_users):
    """Test user registration"""
    response = client.post('/register', data={
        'username': 'newuser',
        'password': 'newpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Registration successful' in response.data

def test_user_login(client, clean_users):
    """Test user login"""
    # First register a user
    users = {
        '1': {
            'username': 'testuser',
            'password': generate_password_hash('testpass')
        }
    }
    save_users(users)
    
    # Try to login
    response = client.post('/login', data={
        'username': 'testuser',
        'password': 'testpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data

def test_user_logout(authenticated_client):
    """Test user logout"""
    response = authenticated_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Logged out successfully' in response.data
