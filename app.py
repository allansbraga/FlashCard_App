from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import os
import datetime
from schema import initialize_database, DATABASE_PATH
from models import Category, Flashcard, User, StudentProgress
import sqlite3
import secrets
import json
import urllib.request, urllib.parse

# Initialize the database
initialize_database()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages and sessions

# Context processor to add variables to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now(), 'csrf_token': session.get('csrf_token')}

@app.before_request
def ensure_csrf():
    if not session.get('csrf_token'):
        session['csrf_token'] = secrets.token_hex(16)

# Initialize models
category_model = Category()
flashcard_model = Flashcard()
user_model = User()
progress_model = StudentProgress()

# Routes
@app.route('/')
def index():
    """Home page showing categories and recent flashcards"""
    uid = session.get('user_id')
    categories = category_model.get_all_categories(user_id=uid)
    uid = session.get('user_id')
    recent_flashcards = flashcard_model.get_all_flashcards(user_id=uid)
    return render_template('index.html', 
                           categories=categories, 
                           recent_flashcards=recent_flashcards[:10] if recent_flashcards else [])

# Category routes
@app.route('/categories')
def list_categories():
    """List all categories"""
    uid = session.get('user_id')
    categories = category_model.get_all_categories(user_id=uid)
    return render_template('categories.html', categories=categories)

@app.route('/categories/add', methods=['GET', 'POST'])
def add_category():
    """Add a new category"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        
        if not name:
            flash('Category name is required', 'error')
            return render_template('category_form.html')
        
        uid = session.get('user_id')
        result = category_model.add_category(name, description, user_id=uid)
        
        if result['success']:
            flash('Category added successfully', 'success')
            return redirect(url_for('list_categories'))
        else:
            flash(result['error'], 'error')
            return render_template('category_form.html', name=name, description=description)
    
    return render_template('category_form.html')

@app.route('/categories/edit/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    """Edit an existing category"""
    category = category_model.get_category_by_id(category_id)
    
    if not category:
        flash('Category not found', 'error')
        return redirect(url_for('list_categories'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        
        if not name:
            flash('Category name is required', 'error')
            return render_template('category_form.html', category=category)
        
        uid = session.get('user_id')
        result = category_model.update_category(category_id, name, description, user_id=uid)
        
        if result['success']:
            flash('Category updated successfully', 'success')
            return redirect(url_for('list_categories'))
        else:
            flash(result['error'], 'error')
            return render_template('category_form.html', category=category, name=name, description=description)
    
    return render_template('category_form.html', category=category)

@app.route('/categories/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    """Delete a category"""
    result = category_model.delete_category(category_id)
    
    if result['success']:
        flash('Category deleted successfully', 'success')
    else:
        flash(result['error'], 'error')
    
    return redirect(url_for('list_categories'))

# Flashcard routes
@app.route('/flashcards')
def list_flashcards():
    """List all flashcards, optionally filtered by category"""
    category_id = request.args.get('category_id', type=int)
    categories = category_model.get_all_categories()
    
    uid = session.get('user_id')
    if category_id:
        flashcards = flashcard_model.get_all_flashcards(category_id, user_id=uid)
        selected_category = category_model.get_category_by_id(category_id)
    else:
        flashcards = flashcard_model.get_all_flashcards(user_id=uid)
        selected_category = None
    
    return render_template('flashcards.html', 
                           flashcards=flashcards, 
                           categories=categories,
                           selected_category=selected_category)

@app.route('/flashcards/add', methods=['GET', 'POST'])
def add_flashcard():
    """Add a new flashcard"""
    categories = category_model.get_all_categories()
    
    if request.method == 'POST':
        front_content = request.form.get('front_content')
        back_content = request.form.get('back_content')
        category_id = request.form.get('category_id')
        
        # Convert empty string to None for category_id
        if category_id == '':
            category_id = None
        else:
            category_id = int(category_id)
        
        if not front_content or not back_content:
            flash('Both front and back content are required', 'error')
            return render_template('flashcard_form.html', categories=categories, 
                                  flashcard={'front_content': front_content, 'back_content': back_content, 'category_id': category_id})
        
        uid = session.get('user_id')
        result = flashcard_model.add_flashcard(front_content, back_content, category_id, user_id=uid)
        
        if result['success']:
            flash('Flashcard added successfully', 'success')
            return redirect(url_for('list_flashcards'))
        else:
            flash(result.get('error', 'Error adding flashcard'), 'error')
            return render_template('flashcard_form.html', categories=categories,
                                   flashcard={'front_content': front_content, 'back_content': back_content, 'category_id': category_id})
    
    return render_template('flashcard_form.html', categories=categories)

@app.route('/flashcards/edit/<int:flashcard_id>', methods=['GET', 'POST'])
def edit_flashcard(flashcard_id):
    """Edit an existing flashcard"""
    flashcard = flashcard_model.get_flashcard_by_id(flashcard_id)
    categories = category_model.get_all_categories()
    
    if not flashcard:
        flash('Flashcard not found', 'error')
        return redirect(url_for('list_flashcards'))
    
    if request.method == 'POST':
        front_content = request.form.get('front_content')
        back_content = request.form.get('back_content')
        category_id = request.form.get('category_id')
        
        # Convert empty string to None for category_id
        if category_id == '':
            category_id = None
        else:
            category_id = int(category_id)
        
        if not front_content or not back_content:
            flash('Both front and back content are required', 'error')
            return render_template('flashcard_form.html', flashcard=flashcard, categories=categories)
        
        uid = session.get('user_id')
        result = flashcard_model.update_flashcard(flashcard_id, front_content, back_content, category_id, user_id=uid)
        
        if result['success']:
            flash('Flashcard updated successfully', 'success')
            return redirect(url_for('list_flashcards'))
        else:
            flash(result.get('error', 'Error updating flashcard'), 'error')
            return render_template('flashcard_form.html', flashcard=flashcard, categories=categories)
    
    return render_template('flashcard_form.html', flashcard=flashcard, categories=categories)

@app.route('/flashcards/delete/<int:flashcard_id>', methods=['POST'])
def delete_flashcard(flashcard_id):
    """Delete a flashcard"""
    result = flashcard_model.delete_flashcard(flashcard_id)
    
    if result['success']:
        flash('Flashcard deleted successfully', 'success')
    else:
        flash('Error deleting flashcard', 'error')
    
    return redirect(url_for('list_flashcards'))

# Review routes
@app.route('/review')
def review():
    """Review flashcards"""
    uid = session.get('user_id')
    cards = flashcard_model.get_cards_for_review(user_id=uid)
    return render_template('review.html', cards=cards)

@app.route('/review/record', methods=['POST'])
def record_review():
    """Record a flashcard review"""
    flashcard_id = request.form.get('flashcard_id', type=int)
    performance_rating = request.form.get('rating', type=int)
    
    if not flashcard_id or not performance_rating:
        return jsonify({'success': False, 'error': 'Missing required parameters'})
    
    result = flashcard_model.record_review(flashcard_id, performance_rating)
    uid = session.get('user_id')
    if uid:
        progress_model.update_progress(uid, 'Vocab', performance_rating)
    return jsonify(result)

# Auth routes
def login_required(fn):
    from functools import wraps
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Authentication required', 'error')
            return redirect(url_for('login'))
        return fn(*args, **kwargs)
    return wrapper

@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        native_language = request.form.get('native_language')
        if not email or not password:
            flash('Email and password are required', 'error')
            return render_template('register.html')
        result = user_model.create_user(email, password, native_language)
        if result['success']:
            user = user_model.get_by_email(email)
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            flash('Registration successful', 'success')
            return redirect(url_for('index'))
        else:
            flash(result.get('error', 'Registration error'), 'error')
            return render_template('register.html', email=email, native_language=native_language)
    return render_template('register.html')

@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        auth = user_model.authenticate(email, password)
        if auth['success']:
            user = auth['user']
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'error')
            return render_template('login.html', email=email)
    return render_template('login.html')

@app.route('/auth/logout')
def logout():
    session.clear()
    flash('Logged out', 'success')
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET'])
@login_required
def profile():
    uid = session.get('user_id')
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE id = ?', (uid,))
    user = cur.fetchone()
    cur.execute('SELECT skill, score, last_session FROM student_progress WHERE user_id = ? ORDER BY skill', (uid,))
    progress = cur.fetchall()
    conn.close()
    return render_template('profile.html', user=user, progress=progress)

# Dashboard routes
@app.route('/dashboard')
def dashboard():
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute('SELECT COUNT(*) AS total FROM flashcards')
    total_cards = cur.fetchone()['total']

    cur.execute("SELECT COUNT(*) AS reviews_7d FROM review_history WHERE reviewed_at >= datetime('now','-7 days')")
    reviews_7d = cur.fetchone()['reviews_7d']

    cur.execute('SELECT AVG(performance_rating) AS avg_rating FROM review_history')
    avg_rating_row = cur.fetchone()
    avg_rating = round(avg_rating_row['avg_rating'], 2) if avg_rating_row and avg_rating_row['avg_rating'] is not None else None

    cur.execute('SELECT category_id, COUNT(*) AS cnt FROM flashcards GROUP BY category_id')
    per_category = cur.fetchall()

    conn.close()

    return render_template('dashboard.html',
                           total_cards=total_cards,
                           reviews_7d=reviews_7d,
                           avg_rating=avg_rating,
                           per_category=per_category,
                           categories=category_model.get_all_categories())

# API routes for AJAX operations
@app.route('/api/flashcards/<int:flashcard_id>')
def get_flashcard(flashcard_id):
    """Get a flashcard by ID (for AJAX)"""
    flashcard = flashcard_model.get_flashcard_by_id(flashcard_id)
    
    if not flashcard:
        return jsonify({'success': False, 'error': 'Flashcard not found'})
    
    # Convert Row to dict
    flashcard_dict = dict(flashcard)
    return jsonify({'success': True, 'flashcard': flashcard_dict})

# Listening
@app.route('/listening')
def listening():
    uid = session.get('user_id')
    diff = progress_model.get_difficulty(uid, 'Listening') if uid else 50
    return render_template('listening.html', difficulty=diff)

@app.route('/api/listening/submit', methods=['POST'])
def listening_submit():
    uid = session.get('user_id')
    if request.form.get('csrf_token') != session.get('csrf_token'):
        return jsonify({'success': False, 'error': 'Invalid CSRF token'})
    correct = request.form.get('correct', type=int)
    delta = 10 if correct else 2
    if uid:
        progress_model.update_progress(uid, 'Listening', delta)
        progress_model.adjust_difficulty(uid, 'Listening', bool(correct))
    return jsonify({'success': True})

# Writing
@app.route('/writing')
def writing():
    return render_template('writing.html')

@app.route('/api/writing/check', methods=['POST'])
def writing_check():
    if request.form.get('csrf_token') != session.get('csrf_token'):
        return jsonify({'success': False, 'error': 'Invalid CSRF token'})
    text = request.form.get('text', '')
    uid = session.get('user_id')
    errors = 0
    score = 0
    try:
        payload = urllib.parse.urlencode({'text': text, 'language': 'en-US'}).encode()
        req = urllib.request.Request('https://api.languagetool.org/v2/check', data=payload)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            matches = data.get('matches', [])
            errors = len(matches)
            score = max(0, 100 - errors * 5)
    except Exception:
        errors = min(len(text)//5, 100)
        score = max(0, 100 - errors)
    if uid:
        progress_model.update_progress(uid, 'Writing', score/10)
    return jsonify({'success': True, 'score': score, 'errors': errors})

# Speaking
@app.route('/speaking')
def speaking():
    return render_template('speaking.html')

@app.route('/api/speaking/submit', methods=['POST'])
def speaking_submit():
    uid = session.get('user_id')
    if request.form.get('csrf_token') != session.get('csrf_token'):
        return jsonify({'success': False, 'error': 'Invalid CSRF token'})
    quality = request.form.get('quality', type=int)
    delta = max(1, min(20, quality or 10))
    if uid:
        progress_model.update_progress(uid, 'Speaking', delta)
    return jsonify({'success': True})

# Personal dashboard
@app.route('/dashboard/me')
def dashboard_me():
    uid = session.get('user_id')
    if not uid:
        flash('Authentication required', 'error')
        return redirect(url_for('login'))
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute('SELECT skill, score, streak_days FROM student_progress WHERE user_id = ? ORDER BY skill', (uid,))
    progress = cur.fetchall()
    badges = []
    for p in progress:
        if p['streak_days'] >= 7:
            badges.append(f"Streak 7d ({p['skill']})")
        if p['score'] >= 100:
            badges.append(f"100+ pontos ({p['skill']})")
    conn.close()
    return render_template('dashboard_me.html', progress=progress, badges=badges)

if __name__ == '__main__':
    # Use environment variables for configuration in production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
