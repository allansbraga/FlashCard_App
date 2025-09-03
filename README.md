# FlashCard App

A Flask-based web application for creating and studying flashcards to memorize languages and other content.

## Features

- Create and manage categories to organize your flashcards
- Create flashcards with front and back content
- Review flashcards with a spaced repetition system
- Track your learning progress
- Responsive design that works on desktop and mobile

## Installation

1. Clone the repository or download the files

2. Create and activate a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Initialize the database (this happens automatically when you run the app for the first time)

2. Run the application:

```bash
python app.py
```

3. Open your web browser and navigate to http://127.0.0.1:5000/

## How to Use

1. **Create Categories**: Start by creating categories to organize your flashcards (e.g., Spanish Vocabulary, Math Formulas)

2. **Create Flashcards**: Add flashcards with front content (question/prompt) and back content (answer/information)

3. **Review**: Use the review system to practice your flashcards. Rate how well you remembered each card to optimize the spaced repetition algorithm.

## Deployment

### Deploying to PythonAnywhere

1. Create a PythonAnywhere account at https://www.pythonanywhere.com/

2. Upload your project files to PythonAnywhere:
   - Use the Files tab to create a new directory (e.g., `flashcard_app`)
   - Upload all project files or use Git to clone your repository

3. Set up a virtual environment and install dependencies:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.9 flashcard_env
   cd ~/flashcard_app
   pip install -r requirements.txt
   ```

4. Configure a new web app:
   - Go to the Web tab and click "Add a new web app"
   - Choose "Manual configuration" and select Python 3.9
   - Set the path to your virtual environment: `/home/yourusername/.virtualenvs/flashcard_env`
   - Set the WSGI configuration file to point to your wsgi.py file

5. Configure the WSGI file:
   - Edit the WSGI configuration file
   - Update the path to your project directory
   - Save the changes

6. Reload your web app and visit your PythonAnywhere URL

## Project Structure

- `app.py`: Main Flask application with routes
- `schema.py`: Database schema definition
- `models.py`: Database models and operations
- `templates/`: HTML templates for the web interface
- `static/`: CSS, JavaScript, and other static files

## License

This project is open source and available for personal and educational use.

## Contributing

Feel free to fork this project and submit pull requests with improvements or bug fixes.