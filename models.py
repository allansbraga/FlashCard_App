import sqlite3
import datetime
from schema import DATABASE_PATH

class DatabaseManager:
    """Class to handle database operations"""
    
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
    
    def get_connection(self):
        """Get a database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # This allows accessing columns by name
        return conn
    
    def close_connection(self, conn):
        """Close the database connection"""
        if conn:
            conn.close()

class Category:
    """Model for flashcard categories"""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
    
    def get_all_categories(self):
        """Get all categories"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM categories ORDER BY name')
        categories = cursor.fetchall()
        
        self.db_manager.close_connection(conn)
        return categories
    
    def get_category_by_id(self, category_id):
        """Get a category by ID"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM categories WHERE id = ?', (category_id,))
        category = cursor.fetchone()
        
        self.db_manager.close_connection(conn)
        return category
    
    def add_category(self, name, description=''):
        """Add a new category"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO categories (name, description) VALUES (?, ?)', 
                          (name, description))
            conn.commit()
            result = {'success': True, 'id': cursor.lastrowid}
        except sqlite3.IntegrityError:
            # Category name already exists
            result = {'success': False, 'error': 'Category name already exists'}
        
        self.db_manager.close_connection(conn)
        return result
    
    def update_category(self, category_id, name, description):
        """Update an existing category"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE categories SET name = ?, description = ? WHERE id = ?', 
                          (name, description, category_id))
            conn.commit()
            result = {'success': True, 'rows_affected': cursor.rowcount}
        except sqlite3.IntegrityError:
            # Category name already exists
            result = {'success': False, 'error': 'Category name already exists'}
        
        self.db_manager.close_connection(conn)
        return result
    
    def delete_category(self, category_id):
        """Delete a category"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Check if there are flashcards in this category
        cursor.execute('SELECT COUNT(*) FROM flashcards WHERE category_id = ?', (category_id,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            result = {'success': False, 'error': f'Cannot delete category with {count} flashcards'}
        else:
            cursor.execute('DELETE FROM categories WHERE id = ?', (category_id,))
            conn.commit()
            result = {'success': True, 'rows_affected': cursor.rowcount}
        
        self.db_manager.close_connection(conn)
        return result

class Flashcard:
    """Model for flashcards"""
    
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()
    
    def get_all_flashcards(self, category_id=None):
        """Get all flashcards, optionally filtered by category"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        if category_id:
            cursor.execute('''
                SELECT f.*, c.name as category_name 
                FROM flashcards f
                LEFT JOIN categories c ON f.category_id = c.id
                WHERE f.category_id = ?
                ORDER BY f.created_at DESC
            ''', (category_id,))
        else:
            cursor.execute('''
                SELECT f.*, c.name as category_name 
                FROM flashcards f
                LEFT JOIN categories c ON f.category_id = c.id
                ORDER BY f.created_at DESC
            ''')
        
        flashcards = cursor.fetchall()
        
        self.db_manager.close_connection(conn)
        return flashcards
    
    def get_flashcard_by_id(self, flashcard_id):
        """Get a flashcard by ID"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT f.*, c.name as category_name 
            FROM flashcards f
            LEFT JOIN categories c ON f.category_id = c.id
            WHERE f.id = ?
        ''', (flashcard_id,))
        
        flashcard = cursor.fetchone()
        
        self.db_manager.close_connection(conn)
        return flashcard
    
    def add_flashcard(self, front_content, back_content, category_id=None):
        """Add a new flashcard"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO flashcards (category_id, front_content, back_content) 
            VALUES (?, ?, ?)
        ''', (category_id, front_content, back_content))
        
        conn.commit()
        result = {'success': True, 'id': cursor.lastrowid}
        
        self.db_manager.close_connection(conn)
        return result
    
    def update_flashcard(self, flashcard_id, front_content, back_content, category_id=None):
        """Update an existing flashcard"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE flashcards 
            SET front_content = ?, back_content = ?, category_id = ? 
            WHERE id = ?
        ''', (front_content, back_content, category_id, flashcard_id))
        
        conn.commit()
        result = {'success': True, 'rows_affected': cursor.rowcount}
        
        self.db_manager.close_connection(conn)
        return result
    
    def delete_flashcard(self, flashcard_id):
        """Delete a flashcard"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # First delete any review history
        cursor.execute('DELETE FROM review_history WHERE flashcard_id = ?', (flashcard_id,))
        
        # Then delete the flashcard
        cursor.execute('DELETE FROM flashcards WHERE id = ?', (flashcard_id,))
        
        conn.commit()
        result = {'success': True, 'rows_affected': cursor.rowcount}
        
        self.db_manager.close_connection(conn)
        return result
    
    def get_cards_for_review(self, limit=20):
        """Get flashcards that are due for review based on spaced repetition"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Get cards that haven't been reviewed or are due for review
        # This is a simple implementation - a more sophisticated algorithm could be used
        cursor.execute('''
            SELECT f.*, c.name as category_name 
            FROM flashcards f
            LEFT JOIN categories c ON f.category_id = c.id
            WHERE f.last_reviewed IS NULL
            OR datetime(f.last_reviewed, '+' || (f.difficulty_level + 1) || ' days') <= datetime('now')
            ORDER BY RANDOM()
            LIMIT ?
        ''', (limit,))
        
        cards = cursor.fetchall()
        
        self.db_manager.close_connection(conn)
        return cards
    
    def record_review(self, flashcard_id, performance_rating):
        """Record a review of a flashcard"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        # Ensure performance rating is between 1 and 5
        performance_rating = max(1, min(5, performance_rating))
        
        # Update the review count and last reviewed timestamp
        cursor.execute('''
            UPDATE flashcards 
            SET review_count = review_count + 1,
                last_reviewed = datetime('now'),
                difficulty_level = CASE
                    WHEN ? >= 4 THEN difficulty_level + 1  -- Increase difficulty if well remembered
                    WHEN ? <= 2 THEN max(0, difficulty_level - 1)  -- Decrease difficulty if poorly remembered
                    ELSE difficulty_level  -- Keep the same if medium performance
                END
            WHERE id = ?
        ''', (performance_rating, performance_rating, flashcard_id))
        
        # Add to review history
        cursor.execute('''
            INSERT INTO review_history (flashcard_id, performance_rating)
            VALUES (?, ?)
        ''', (flashcard_id, performance_rating))
        
        conn.commit()
        result = {'success': True}
        
        self.db_manager.close_connection(conn)
        return result