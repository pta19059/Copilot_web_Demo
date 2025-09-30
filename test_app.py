import pytest
from app import app, load_history, save_submission, HISTORY_FILE
import os
import json
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
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

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Copilot Demo" in response.data

def test_form_submission(client, clean_history):
    response = client.post("/", data={"name": "Alice"})
    assert response.status_code == 200
    assert b"Alice" in response.data
    assert b"Your submission has been logged" in response.data

def test_history_page_empty(client, clean_history):
    """Test history page when no submissions exist"""
    response = client.get('/history')
    assert response.status_code == 200
    assert b'No submissions yet' in response.data

def test_history_page_with_submissions(client, clean_history):
    """Test history page with submissions"""
    # First make a submission
    client.post('/', data={'name': 'Test User'})
    
    # Check history page
    response = client.get('/history')
    assert response.status_code == 200
    assert b'Test User' in response.data
    assert b'Total Submissions' in response.data

def test_clear_history(client, clean_history):
    """Test clearing submission history"""
    # Make a submission first
    client.post('/', data={'name': 'Test User'})
    
    # Clear history
    response = client.post('/clear-history')
    assert response.status_code == 302  # Redirect response
    
    # Check that history is empty
    response = client.get('/history')
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

def test_logging_file_creation(client, clean_history):
    """Test that submissions create log entries"""
    # Make a submission
    client.post('/', data={'name': 'Log Test User'})
    
    # Check that log file exists (submissions.log)
    assert os.path.exists('submissions.log')
    
    # Read log file and check for entry
    with open('submissions.log', 'r') as f:
        log_content = f.read()
        assert 'Log Test User' in log_content
        assert 'New submission' in log_content
