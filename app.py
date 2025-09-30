from flask import Flask, render_template, request, redirect, url_for # type: ignore
import logging
import json
import os
from datetime import datetime

app = Flask(__name__)

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
def index_post():
    name = request.form.get('name', '').strip()
    
    if name:
        # Save the submission to history and log it
        save_submission(name)
        return render_template('index.html', name=name)
    else:
        return render_template('index.html', form_name=request.form.get('name', ''))

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
    app.run(debug=True)
