from flask import Flask, render_template, request, redirect, url_for
import os
from pyresparser import ResumeParser  # For resume parsing

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Mock database (replace with SQLite/SQLAlchemy later)
users = {
    "test@email.com": {
        "password": "123",
        "resume_skills": [],
        "applications": []
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    if email in users and users[email]['password'] == password:
        return redirect(url_for('dashboard'))
    return "Login failed!"

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=users["test@email.com"])

@app.route('/upload', methods=['POST'])
def upload_resume():
    resume = request.files['resume']
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
    resume.save(resume_path)
    
    # Parse resume (simplified)
    data = ResumeParser(resume_path).get_extracted_data()
    users["test@email.com"]["resume_skills"] = data.get('skills', [])
    
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
