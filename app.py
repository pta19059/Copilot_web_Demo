from flask import Flask, render_template, request, redirect, url_for # type: ignore
from flask_wtf.csrf import CSRFProtect # type: ignore
from markupsafe import escape # type: ignore
import logging
import json
import os
import secrets
from datetime import datetime

app = Flask(__name__)

# Security: Set a secret key for session management and CSRF protection
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or secrets.token_hex(32)

# Security: Enable CSRF protection
csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('submissions.log'),
        logging.StreamHandler()
    ]
)

# File to store submission history
HISTORY_FILE = 'submission_history.json'

@app.after_request
def add_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self' https://fonts.googleapis.com https://fonts.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com"
    return response

def load_history():
    """Load submission history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def sanitize_input(text, max_length=50):
    """Sanitize user input to prevent security issues"""
    if not text or not isinstance(text, str):
        return ''
    
    # Strip whitespace
    text = text.strip()
    
    # Limit length
    text = text[:max_length]
    
    # Escape HTML to prevent XSS
    # markupsafe.escape handles all dangerous characters
    text = escape(text)
    
    return text

def save_submission(name):
    """Save a submission to history and log it"""
    timestamp = datetime.now().isoformat()
    
    # Load existing history
    history = load_history()
    
    # Add new submission
    submission = {
        'name': name,
        'timestamp': timestamp,
        'formatted_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    history.append(submission)
    
    # Save to file
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    except IOError as e:
        app.logger.error(f"Failed to save submission history: {e}")
    
    # Log the submission (sanitize for log injection prevention)
    safe_name = name.replace('\n', ' ').replace('\r', ' ')
    app.logger.info(f"New submission: {safe_name} at {timestamp}")

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/', methods=['POST'])
def index_post():
    """Handle form submission with input validation and sanitization"""
    name = request.form.get('name', '')
    
    # Security: Validate and sanitize input
    if name:
        # Additional validation on stripped input
        name_stripped = name.strip()
        if len(name_stripped) < 2:
            sanitized_form_name = sanitize_input(name_stripped)
            return render_template('index.html', form_name=sanitized_form_name, error='Name must be at least 2 characters long')
        elif len(name_stripped) > 50:
            sanitized_form_name = sanitize_input(name_stripped[:50])
            return render_template('index.html', form_name=sanitized_form_name, error='Name must be 50 characters or less')
        else:
            # Sanitize the input
            sanitized_name = sanitize_input(name_stripped)
            # Save the submission to history and log it
            save_submission(sanitized_name)
            return render_template('index.html', name=sanitized_name)
    else:
        sanitized_form_name = sanitize_input(request.form.get('name', ''))
        return render_template('index.html', form_name=sanitized_form_name)

@app.route('/history')
def history():
    """Display submission history"""
    submissions = load_history()
    # Reverse to show most recent first
    submissions.reverse()
    return render_template('history.html', submissions=submissions)

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Clear submission history"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        app.logger.info("Submission history cleared")
    except IOError as e:
        app.logger.error(f"Failed to clear submission history: {e}")
    
    return redirect(url_for('history'))

if __name__ == '__main__':
    # Security: Only enable debug mode if explicitly set via environment variable
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
