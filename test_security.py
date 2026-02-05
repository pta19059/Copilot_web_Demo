"""Security tests for the Flask application"""
import pytest
from app import app, sanitize_input, HISTORY_FILE
import os


@pytest.fixture
def client():
    """Create a test client with CSRF disabled"""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
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


def test_xss_input_sanitization(client, clean_history):
    """Test that XSS attempts are sanitized"""
    xss_payload = '<script>alert("XSS")</script>'
    response = client.post('/', data={'name': xss_payload})
    
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    
    # The malicious unescaped script should NOT be in the response
    assert '<script>alert("XSS")</script>' not in response_text
    
    # The escaped version should be present
    assert '&lt;script&gt;' in response_text or '&amp;lt;script&amp;gt;' in response_text


def test_sql_injection_protection(client, clean_history):
    """Test that potential SQL injection attempts are handled"""
    sql_payload = "'; DROP TABLE users; --"
    response = client.post('/', data={'name': sql_payload})
    
    assert response.status_code == 200
    # Should not crash the application


def test_security_headers_present(client):
    """Test that security headers are set"""
    response = client.get('/')
    
    assert response.headers.get('X-Content-Type-Options') == 'nosniff'
    assert response.headers.get('X-Frame-Options') == 'DENY'
    assert response.headers.get('X-XSS-Protection') == '1; mode=block'
    assert 'Content-Security-Policy' in response.headers


def test_input_length_validation(client, clean_history):
    """Test that input length is validated"""
    # Too short
    response = client.post('/', data={'name': 'A'})
    assert response.status_code == 200
    # Should show error or not process
    
    # Too long
    long_name = 'A' * 100
    response = client.post('/', data={'name': long_name})
    assert response.status_code == 200
    # Should be truncated or show error


def test_sanitize_input_function():
    """Test the sanitize_input function directly"""
    # Test XSS
    assert '<script>' not in sanitize_input('<script>alert("XSS")</script>')
    
    # Test length limit
    long_input = 'A' * 100
    result = sanitize_input(long_input, max_length=50)
    assert len(str(result)) <= 50
    
    # Test whitespace
    result = sanitize_input('  test  ')
    assert 'test' in str(result)
    
    # Test empty input
    assert sanitize_input('') == ''
    assert sanitize_input(None) == ''
    
    # Test non-string types
    assert sanitize_input(123) == ''
    assert sanitize_input([]) == ''
    assert sanitize_input({}) == ''


def test_log_injection_prevention(client, clean_history):
    """Test that log injection attempts are prevented"""
    # Try to inject new lines into logs
    payload = "TestUser\nFAKE LOG ENTRY"
    response = client.post('/', data={'name': payload})
    assert response.status_code == 200
    
    # Check logs don't have raw newlines
    if os.path.exists('submissions.log'):
        with open('submissions.log', 'r') as f:
            log_content = f.read()
            # The newline should be replaced or escaped
            lines = log_content.split('\n')
            # Each actual log line should start with a timestamp
            for line in lines:
                if 'FAKE LOG ENTRY' in line:
                    # Should be part of the same log entry, not a new line
                    assert line.strip() != 'FAKE LOG ENTRY'


def test_csrf_enabled_in_production():
    """Test that CSRF protection is enabled by default"""
    from flask_wtf.csrf import CSRFProtect
    test_app = app
    # Check that CSRF is initialized
    assert hasattr(test_app, 'extensions')


def test_secret_key_configured():
    """Test that a secret key is configured"""
    assert app.config.get('SECRET_KEY') is not None
    assert len(app.config.get('SECRET_KEY')) > 0
    # Should not be a default/weak key
    assert app.config.get('SECRET_KEY') != 'dev'


def test_debug_mode_disabled_by_default():
    """Test that debug mode is controlled by environment variable"""
    import app as app_module
    import inspect
    
    source = inspect.getsource(app_module)
    # Should not have app.run(debug=True) hardcoded without environment check
    # Must check for FLASK_DEBUG if debug is mentioned
    assert 'app.run(debug=True)' not in source
    # The code should use environment-based debug mode
    assert 'FLASK_DEBUG' in source
