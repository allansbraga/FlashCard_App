import sqlite3
import os

# Use environment variable for database path or default to 'flashcards.db'
DATABASE_PATH = os.environ.get('DATABASE_PATH', 'flashcards.db')

def create_tables():
    """Create the necessary tables for the flashcard application"""
    # Check if database file exists
    db_exists = os.path.exists(DATABASE_PATH)
    
    # Connect to database (creates it if it doesn't exist)
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create categories table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        user_id INTEGER
    )
    ''')
    
    # Create flashcards table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS flashcards (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        front_content TEXT NOT NULL,
        back_content TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_reviewed TIMESTAMP,
        review_count INTEGER DEFAULT 0,
        difficulty_level INTEGER DEFAULT 0,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')
    
    # Create review history table for spaced repetition
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS review_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flashcard_id INTEGER,
        reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        performance_rating INTEGER,  -- 1-5 rating of how well the user remembered
        FOREIGN KEY (flashcard_id) REFERENCES flashcards (id)
    )
    ''')

    # Add SRS columns to flashcards if they do not exist
    def column_exists(table_name, column_name):
        cursor.execute(f"PRAGMA table_info({table_name})")
        return any(row[1] == column_name for row in cursor.fetchall())

    if not column_exists('flashcards', 'ease_factor'):
        cursor.execute("ALTER TABLE flashcards ADD COLUMN ease_factor REAL DEFAULT 2.5")
    if not column_exists('flashcards', 'interval_days'):
        cursor.execute("ALTER TABLE flashcards ADD COLUMN interval_days INTEGER DEFAULT 1")
    if not column_exists('flashcards', 'next_review_at'):
        cursor.execute("ALTER TABLE flashcards ADD COLUMN next_review_at TIMESTAMP")

    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        native_language TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Create student progress table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_progress (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        skill TEXT NOT NULL,
        score REAL DEFAULT 0,
        last_session TIMESTAMP,
        streak_days INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # Add user_id to flashcards for multi-tenant support
    if not column_exists('flashcards', 'user_id'):
        cursor.execute("ALTER TABLE flashcards ADD COLUMN user_id INTEGER")
    
    # Commit changes and close connection
    conn.commit()
    conn.close()
    
    return db_exists

def initialize_database():
    """Initialize the database with default categories if needed"""
    db_exists = create_tables()
    
    # If this is a new database, add some default categories
    if not db_exists:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Insert default categories
        default_categories = [
            ('Languages', 'Vocabulary and phrases for language learning'),
            ('General Knowledge', 'Facts and information for general learning'),
            ('Programming', 'Programming concepts and syntax')
        ]
        
        cursor.executemany('INSERT INTO categories (name, description) VALUES (?, ?)', 
                          default_categories)
        
        conn.commit()
        conn.close()
        
        print("Database initialized with default categories.")
    else:
        print("Using existing database.")

if __name__ == "__main__":
    initialize_database()