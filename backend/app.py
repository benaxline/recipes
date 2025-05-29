# backend/app.py

import os
import sys
import traceback
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from utils.sheets import get_recipes   # your helper

# make sure backend/ is on the path so we can import sheets.py
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)

# Configure Flask to serve the frontend directory
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
app = Flask(__name__,
            static_folder=FRONTEND_DIR,
            static_url_path='')  # serve at /

CORS(app)  # allow cross-origin; optional if you serve everything from this origin

# database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(PROJECT_ROOT, 'recipes.db')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_frontend(path):
    full_path = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(full_path):
        return send_from_directory(FRONTEND_DIR, path)
    # if not a frontend file, return 404 so Flask can try other routes
    return jsonify({'error': 'Not found'}), 404

# @app.route('/')
# def serve_index():
#     # default to recipes.html as the home page
#     return send_from_directory(FRONTEND_DIR, 'recipes.html')

# @app.route('/recipes.html')
# def serve_recipes_html():
#     return send_from_directory(FRONTEND_DIR, 'recipes.html')

# @app.route('/recipe-detail.html')
# def serve_detail_html():
#     return send_from_directory(FRONTEND_DIR,'recipe-detail.html')

@app.route('/api/recipes', methods=['GET'])
def api_list_recipes():
    try:
        recipes = get_recipes()
        return jsonify(recipes), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/recipes/<string:name>', methods=['GET'])
def api_get_recipe(name):
    try:
        recipes = get_recipes()
        for r in recipes:
            if r.get('name', '').lower() == name.lower():
                return jsonify(r), 200
        return jsonify({'error': f'Recipe "{name}" not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # enable debug and auto-reload on changes
    app.run(host='0.0.0.0', port=5005, debug=True)
