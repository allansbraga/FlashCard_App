from schema import create_tables, initialize_database

if __name__ == '__main__':
    print('Initializing database...')
    initialize_database()
    print('Database initialized successfully!')