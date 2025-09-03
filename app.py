from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import datetime
from schema import initialize_database
from models import Category, Flashcard

# Initialize the database
initialize_database()

# Create Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages and sessions

# Context processor to add variables to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.datetime.now()}

# Initialize models
category_model = Category()
flashcard_model = Flashcard()

# Routes
@app.route('/')
def index():
    """Home page showing categories and recent flashcards"""
    categories = category_model.get_all_categories()
    recent_flashcards = flashcard_model.get_all_flashcards()
    return render_template('index.html', 
                           categories=categories, 
                           recent_flashcards=recent_flashcards[:10] if recent_flashcards else [])

# Category routes
@app.route('/categories')
def list_categories():
    """List all categories"""
    categories = category_model.get_all_categories()
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
        
        result = category_model.add_category(name, description)
        
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
        
        result = category_model.update_category(category_id, name, description)
        
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
    
    if category_id:
        flashcards = flashcard_model.get_all_flashcards(category_id)
        selected_category = category_model.get_category_by_id(category_id)
    else:
        flashcards = flashcard_model.get_all_flashcards()
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
        
        result = flashcard_model.add_flashcard(front_content, back_content, category_id)
        
        if result['success']:
            flash('Flashcard added successfully', 'success')
            return redirect(url_for('list_flashcards'))
    
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
        
        result = flashcard_model.update_flashcard(flashcard_id, front_content, back_content, category_id)
        
        if result['success']:
            flash('Flashcard updated successfully', 'success')
            return redirect(url_for('list_flashcards'))
    
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
    cards = flashcard_model.get_cards_for_review()
    return render_template('review.html', cards=cards)

@app.route('/review/record', methods=['POST'])
def record_review():
    """Record a flashcard review"""
    flashcard_id = request.form.get('flashcard_id', type=int)
    performance_rating = request.form.get('rating', type=int)
    
    if not flashcard_id or not performance_rating:
        return jsonify({'success': False, 'error': 'Missing required parameters'})
    
    result = flashcard_model.record_review(flashcard_id, performance_rating)
    return jsonify(result)

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

if __name__ == '__main__':
    # Use environment variables for configuration in production
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)