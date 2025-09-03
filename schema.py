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
        description TEXT
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