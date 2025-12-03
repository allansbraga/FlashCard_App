import sqlite3
import datetime
from schema import DATABASE_PATH
import os, hashlib, binascii

def _hash_password(password):
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return 'pbkdf2$' + binascii.hexlify(salt).decode() + '$' + binascii.hexlify(dk).decode()

def _check_password(stored, password):
    try:
        prefix, salt_hex, hash_hex = stored.split('$')
        salt = binascii.unhexlify(salt_hex.encode())
        dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        return binascii.hexlify(dk).decode() == hash_hex
    except Exception:
        return False

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
    
    def get_all_categories(self, user_id=None):
        """Get all categories"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        if user_id is not None:
            cursor.execute('SELECT * FROM categories WHERE COALESCE(user_id, -1) = COALESCE(?, -1) ORDER BY name', (user_id,))
        else:
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
    
    def add_category(self, name, description='', user_id=None):
        """Add a new category"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('INSERT INTO categories (name, description, user_id) VALUES (?, ?, ?)', 
                          (name, description, user_id))
            conn.commit()
            result = {'success': True, 'id': cursor.lastrowid}
        except sqlite3.IntegrityError:
            # Category name already exists
            result = {'success': False, 'error': 'Category name already exists'}
        
        self.db_manager.close_connection(conn)
        return result
    
    def update_category(self, category_id, name, description, user_id=None):
        """Update an existing category"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('UPDATE categories SET name = ?, description = ?, user_id = ? WHERE id = ?', 
                          (name, description, user_id, category_id))
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
    
    def get_all_flashcards(self, category_id=None, user_id=None):
        """Get all flashcards, optionally filtered by category"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        
        if category_id and user_id is not None:
            cursor.execute('''
                SELECT f.*, c.name as category_name 
                FROM flashcards f
                LEFT JOIN categories c ON f.category_id = c.id
                WHERE f.category_id = ? AND COALESCE(f.user_id, -1) = COALESCE(?, -1)
                ORDER BY f.created_at DESC
            ''', (category_id, user_id))
        elif category_id:
            cursor.execute('''
                SELECT f.*, c.name as category_name 
                FROM flashcards f
                LEFT JOIN categories c ON f.category_id = c.id
                WHERE f.category_id = ?
                ORDER BY f.created_at DESC
            ''', (category_id,))
        elif user_id is not None:
            cursor.execute('''
                SELECT f.*, c.name as category_name 
                FROM flashcards f
                LEFT JOIN categories c ON f.category_id = c.id
                WHERE COALESCE(f.user_id, -1) = COALESCE(?, -1)
                ORDER BY f.created_at DESC
            ''', (user_id,))
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
    
    def add_flashcard(self, front_content, back_content, category_id=None, user_id=None):
        """Add a new flashcard"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        # Prevent duplicates (case-insensitive, trimmed) within same category
        cursor.execute('''
            SELECT id FROM flashcards
            WHERE COALESCE(category_id, -1) = COALESCE(?, -1)
              AND COALESCE(user_id, -1) = COALESCE(?, -1)
              AND LOWER(TRIM(front_content)) = LOWER(TRIM(?))
              AND LOWER(TRIM(back_content)) = LOWER(TRIM(?))
        ''', (category_id, user_id, front_content, back_content))
        existing = cursor.fetchone()

        if existing:
            result = {'success': False, 'error': 'Duplicate flashcard for this category'}
        else:
            cursor.execute('''
                INSERT INTO flashcards (category_id, front_content, back_content, user_id) 
                VALUES (?, ?, ?, ?)
            ''', (category_id, front_content, back_content, user_id))
            conn.commit()
            result = {'success': True, 'id': cursor.lastrowid}
        
        self.db_manager.close_connection(conn)
        return result
    
    def update_flashcard(self, flashcard_id, front_content, back_content, category_id=None, user_id=None):
        """Update an existing flashcard"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()
        # Prevent updating to a duplicate of another record
        cursor.execute('''
            SELECT id FROM flashcards
            WHERE id != ?
              AND COALESCE(category_id, -1) = COALESCE(?, -1)
              AND COALESCE(user_id, -1) = COALESCE(?, -1)
              AND LOWER(TRIM(front_content)) = LOWER(TRIM(?))
              AND LOWER(TRIM(back_content)) = LOWER(TRIM(?))
        ''', (flashcard_id, category_id, user_id, front_content, back_content))
        existing = cursor.fetchone()

        if existing:
            result = {'success': False, 'error': 'Duplicate flashcard for this category'}
        else:
            cursor.execute('''
                UPDATE flashcards 
                SET front_content = ?, back_content = ?, category_id = ?, user_id = ? 
                WHERE id = ?
            ''', (front_content, back_content, category_id, user_id, flashcard_id))
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
    
    def get_cards_for_review(self, limit=20, user_id=None):
        """Get flashcards due for review using SRS (SM-2)"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()

        if user_id is not None:
            cursor.execute('''
                SELECT f.*, c.name as category_name
                FROM flashcards f
                LEFT JOIN categories c ON f.category_id = c.id
                WHERE COALESCE(f.user_id, -1) = COALESCE(?, -1)
                  AND (f.next_review_at IS NULL OR datetime(f.next_review_at) <= datetime('now'))
                ORDER BY CASE WHEN f.next_review_at IS NULL THEN 0 ELSE 1 END, RANDOM()
                LIMIT ?
            ''', (user_id, limit))
        else:
            cursor.execute('''
                SELECT f.*, c.name as category_name
                FROM flashcards f
                LEFT JOIN categories c ON f.category_id = c.id
                WHERE f.next_review_at IS NULL
                   OR datetime(f.next_review_at) <= datetime('now')
                ORDER BY CASE WHEN f.next_review_at IS NULL THEN 0 ELSE 1 END, RANDOM()
                LIMIT ?
            ''', (limit,))

        cards = cursor.fetchall()
        self.db_manager.close_connection(conn)
        return cards
    
    def record_review(self, flashcard_id, performance_rating):
        """Record a review using SM-2 and schedule next review"""
        conn = self.db_manager.get_connection()
        cursor = conn.cursor()

        # Clamp rating 1..5
        q = max(1, min(5, performance_rating))

        # Fetch current EF and interval
        cursor.execute('SELECT review_count, ease_factor, interval_days FROM flashcards WHERE id = ?', (flashcard_id,))
        row = cursor.fetchone()
        if not row:
            self.db_manager.close_connection(conn)
            return {'success': False, 'error': 'Flashcard not found'}

        review_count = row['review_count'] if isinstance(row, sqlite3.Row) else row[0]
        ease_factor = row['ease_factor'] if isinstance(row, sqlite3.Row) else row[1]
        interval_days = row['interval_days'] if isinstance(row, sqlite3.Row) else row[2]

        if ease_factor is None:
            ease_factor = 2.5
        if interval_days is None:
            interval_days = 1

        # SM-2 EF update (min 1.3)
        ef_delta = 0.1 - (5 - q) * (0.08 + (5 - q) * 0.02)
        new_ef = max(1.3, ease_factor + ef_delta)

        # Interval scheduling
        if q < 3:
            new_interval = 1
            new_review_count = review_count + 1
        else:
            if review_count == 0:
                new_interval = 1
            elif review_count == 1:
                new_interval = 6
            else:
                new_interval = int(round(interval_days * new_ef))
            new_review_count = review_count + 1

        # Compute next review date
        cursor.execute('''
            UPDATE flashcards SET
                review_count = ?,
                last_reviewed = datetime('now'),
                ease_factor = ?,
                interval_days = ?,
                next_review_at = datetime('now', '+' || ? || ' days')
            WHERE id = ?
        ''', (new_review_count, new_ef, new_interval, new_interval, flashcard_id))

        # History
        cursor.execute('INSERT INTO review_history (flashcard_id, performance_rating) VALUES (?, ?)', (flashcard_id, q))

        conn.commit()
        result = {'success': True}
        self.db_manager.close_connection(conn)
        return result

class User:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()

    def create_user(self, email, password, native_language=None):
        conn = self.db_manager.get_connection()
        cur = conn.cursor()
        try:
            cur.execute('INSERT INTO users (email, password_hash, native_language) VALUES (?, ?, ?)',
                        (email, _hash_password(password), native_language))
            conn.commit()
            result = {'success': True, 'id': cur.lastrowid}
        except sqlite3.IntegrityError:
            result = {'success': False, 'error': 'Email already registered'}
        self.db_manager.close_connection(conn)
        return result

    def get_by_email(self, email):
        conn = self.db_manager.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cur.fetchone()
        self.db_manager.close_connection(conn)
        return user

    def authenticate(self, email, password):
        user = self.get_by_email(email)
        if not user:
            return {'success': False, 'error': 'Invalid credentials'}
        ok = _check_password(user['password_hash'], password)
        if ok:
            return {'success': True, 'user': user}
        return {'success': False, 'error': 'Invalid credentials'}

class StudentProgress:
    def __init__(self, db_manager=None):
        self.db_manager = db_manager or DatabaseManager()

    def update_progress(self, user_id, skill, delta_score):
        conn = self.db_manager.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT id, score, streak_days FROM student_progress WHERE user_id = ? AND skill = ?', (user_id, skill))
        row = cur.fetchone()
        if row:
            new_score = (row['score'] if isinstance(row, sqlite3.Row) else row[1]) + delta_score
            cur.execute("""
                UPDATE student_progress 
                SET score = ?, 
                    last_session = datetime('now'),
                    streak_days = CASE 
                        WHEN date(last_session) = date('now','-1 day') THEN streak_days + 1
                        WHEN date(last_session) = date('now') THEN streak_days
                        ELSE 1
                    END
                WHERE id = ?
            """, (new_score, row['id'] if isinstance(row, sqlite3.Row) else row[0]))
        else:
            cur.execute("INSERT INTO student_progress (user_id, skill, score, last_session, streak_days) VALUES (?, ?, ?, datetime('now'), 1)", (user_id, skill, delta_score))
        conn.commit()
        self.db_manager.close_connection(conn)