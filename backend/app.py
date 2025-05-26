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
    if path and os.path.exists(os.path.join('../frontend', path)):
        return send_from_directory('../frontend', path)
    else:
        return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)