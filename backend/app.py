from flask import Flask, send_from_directory
from flask_cors import CORS
from blog_api import blog_bp
from recipe_api import recipe_bp
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(blog_bp)
app.register_blueprint(recipe_bp)

# Serve frontend files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    # Print for debugging
    print(f"Requested path: {path}")
    
    # Check if the file exists in the frontend directory
    frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')
    file_path = os.path.join(frontend_dir, path)
    
    if path and os.path.exists(file_path) and os.path.isfile(file_path):
        # If the file exists, serve it directly
        directory, filename = os.path.split(file_path)
        return send_from_directory(directory, filename)
    else:
        # Otherwise serve index.html
        return send_from_directory(frontend_dir, 'index.html')

if __name__ == '__main__':
    app.run(debug=True)