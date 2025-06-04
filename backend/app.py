# backend/app.py

import os
import traceback
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from supabase import create_client, Client

# load .env file
load_dotenv()

# 1. Create the app and configure it
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')

app = Flask(__name__,
            static_folder=FRONTEND_DIR,
            static_url_path='')
CORS(app)

# initialize supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError('Supabase URL and key must be set in .env file')
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)


# —— Static file serving —— #
@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_frontend(path):
    """
    Serve static files from the frontend directory.
    """
    full = os.path.join(FRONTEND_DIR, path)
    if os.path.isfile(full):
        return send_from_directory(FRONTEND_DIR, path)
    return jsonify({'error': 'Not found'}), 404

# —— API: List all recipes —— #
@app.route('/api/recipes', methods=['GET'])
def api_list_recipes():
    """
    Fetch all recipes from Supabase
    splits newlines in ingredients and instructions
    orders by created_at descending
    returns 200 with list of recipes
    returns 500 with error message on error
    """
    try:
        resp = (
            supabase
            .from_('Recipes')
            .select('*')
            .order('created_at')#, ascending=True)
            .execute()
        )
        data = resp.data
        for recipe in data:
            recipe['ingredients'] = recipe.get('ingredients', '').split('\n') if recipe.get('ingredients') else []
            recipe['instructions'] = recipe.get('instructions', '').split('\n') if recipe.get('instructions') else []
        return jsonify(data), 200
        
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# —— API: Get one by name —— #
@app.route('/api/recipes/<string:name>', methods=['GET'])
def api_get_recipe(name):
    """
    Get a recipe by name.
    
    Args:
        name (str): The name of the recipe.
    
    Returns:
        dict: The recipe.
    """
    try:
        resp = (
            supabase
            .from_('Recipes')
            .select('*')
            .ilike('name', name)
            .execute()
        )
        data = resp.data or []
        if not data:
            return jsonify({'error': f'Recipe \"{name}\" not found'}), 404
        recipe = data[0]
        r['ingredients'] = recipe.get('ingredients', '').split('\n') if recipe.get('ingredients') else []
        r['instructions'] = recipe.get('instructions', '').split('\n') if recipe.get('instructions') else []
        return jsonify(recipe), 200


    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# —— API: Create new recipe —— #
@app.route('/api/recipes', methods=['POST'])
def api_create_recipe():
    """
    Create a new recipe.
    
    Returns:
        dict: The created recipe.
    """
   
    data = request.get_json() or {}
    if not data.get('name') or not data.get('ingredients') or not data.get('instructions'):
        return jsonify({'error': 'name, ingredients, and instructions are required'}), 400
    

    try:
        dup = (
            supabase
            .from_('Recipes')
            .select('id')
            .eq('name', data['name'])
            .eq('author', data.get('author'))
            .limit(1)
            .execute()
        )
        if dup.data:
            return jsonify({'error': 'Recipe already exists'}), 409
        
        payload = {
            'name': data['name'],
            'author': data.get('author'),
            'type': data.get('type'),
            'ingredients': '\n'.join(data['ingredients']),
            'instructions': '\n'.join(data['instructions'])
        }

        insert_resp = supabase.from_('Recipes').insert(payload).execute()
        new_recipe = insert_resp.data[0]
        new_recipe['ingredients'] = new_recipe.get('ingredients', '').split('\n') if new_recipe.get('ingredients') else []
        new_recipe['instructions'] = new_recipe.get('instructions', '').split('\n') if new_recipe.get('instructions') else []
        return jsonify(new_recipe), 201
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500
    

# —— API: Update existing recipe —— #
@app.route('/api/recipes/<int:id>', methods=['PUT'])
def api_update_recipe(id):
    """
    Update an existing recipe.
    
    Args:
        id (int): The ID of the recipe.
    
    Returns:
        dict: The updated recipe.
    """
    data = request.get_json() or {}
    if not data.get('name') or not data.get('ingedients') or not data.get('instructions'):
        return jsonify({'error':'name, ingredients, and instructions are required'}), 400
    try:
        getr = supabase.from_('Recipes').select('*').eq('id', id).limit(1).execute()
        if not getr.data:
            return jsonify({'error':'Not found'}), 404
        
        dup = (
            supabase
            .from_('Recipes')
            .select('id')
            .eq('name', data['name'])
            .eq('author', data.get('author'))
            .neq('id', id)
            .limit(1)
            .execute()
        )
        if dup.data:
            return jsonify({'error':'Another recipe with that name exists'}), 409
        
        payload = {
            'name': data['name'],
            'author': data.get('author'),
            'type': data.get('type'),
            'ingredients': '\n'.join(data['ingredients']),
            'instructions': '\n'.join(data['instructions'])
        }
        
        update_resp = supabase.from_('Recipes').update(payload).eq('id', id).execute()
        updated_recipe = update_resp.data[0]
        updated_recipe['ingredients'] = updated_recipe.get('ingredients', '').split('\n') if updated_recipe.get('ingredients') else []
        updated_recipe['instructions'] = updated_recipe.get('instructions', '').split('\n') if updated_recipe.get('instructions') else []
        return jsonify(updated_recipe), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

# —— API: Delete recipe —— #
@app.route('/api/recipes/<int:id>', methods=['DELETE'])
def api_delete_recipe(id):
    """
    Delete a recipe.
    
    Args:
        id (int): The ID of the recipe.
    
    Returns:
        dict: A message indicating success or failure.
    """
    try:
        getr = supabase.from_('Recipes').select('id').eq('id', id).limit(1).execute()
        if not getr.data:
            return jsonify({'error':'Not found'}), 404
        
        supabase.from_('Recipes').delete().eq('id', id).execute()
        return jsonify({'message':'Deleted'}), 200
    
    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
