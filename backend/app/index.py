from app.main import app
import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'app'))

try:
    from main import app  # Now it will look in the app directory
    print("Successfully imported app from main")
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def home():
        return "API is running - fallback mode"

# Vercel requirement
handler = app