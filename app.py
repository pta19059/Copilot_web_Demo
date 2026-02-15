from flask import Flask, render_template, request, redirect, url_for, flash # type: ignore
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user # type: ignore
import logging
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'  # Change this in production

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

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
USERS_FILE = 'users.json'

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

# In-memory user storage (loaded from file)
def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_users(users):
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
    except IOError as e:
        app.logger.error(f"Failed to save users: {e}")

@login_manager.user_loader
def load_user(user_id):
    users = load_users()
    if user_id in users:
        return User(user_id, users[user_id]['username'])
    return None

def load_history():
    """Load submission history from JSON file"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

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
    
    # Log the submission
    app.logger.info(f"New submission: {name} at {timestamp}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
@login_required
def index_post():
    name = request.form.get('name', '').strip()
    
    if name:
        # Save the submission to history and log it
        save_submission(name)
        return render_template('index.html', name=name)
    else:
        return render_template('index.html', form_name=request.form.get('name', ''))

@app.route('/history')
@login_required
def history():
    """Display submission history"""
    submissions = load_history()
    # Reverse to show most recent first
    submissions.reverse()
    return render_template('history.html', submissions=submissions)

@app.route('/clear-history', methods=['POST'])
@login_required
def clear_history():
    """Clear submission history"""
    try:
        if os.path.exists(HISTORY_FILE):
            os.remove(HISTORY_FILE)
        app.logger.info("Submission history cleared")
    except IOError as e:
        app.logger.error(f"Failed to clear submission history: {e}")
    
    return redirect(url_for('history'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        users = load_users()
        
        # Find user by username
        user_id = None
        for uid, user_data in users.items():
            if user_data['username'] == username:
                user_id = uid
                break
        
        if user_id and check_password_hash(users[user_id]['password'], password):
            user = User(user_id, username)
            login_user(user)
            flash('Logged in successfully!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('register.html')
        
        users = load_users()
        
        # Check if username already exists
        for user_data in users.values():
            if user_data['username'] == username:
                flash('Username already exists', 'error')
                return render_template('register.html')
        
        # Create new user
        user_id = str(len(users) + 1)
        users[user_id] = {
            'username': username,
            'password': generate_password_hash(password)
        }
        save_users(users)
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
