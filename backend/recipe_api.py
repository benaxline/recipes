from flask import Blueprint, jsonify, request
from utils.sheets import get_recipes

recipe_bp = Blueprint('recipe_bp', __name__)

@recipe_bp.route('/recipes', methods=['GET'])
def get_all_recipes():
    """Get all recipes from Google Sheets"""
    try:
        recipes = get_recipes()
        return jsonify(recipes)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@recipe_bp.route('/recipes/<string:name>', methods=['GET'])
def get_recipe(name):
    """Get a specific recipe by name"""
    try:
        recipes = get_recipes()
        for recipe in recipes:
            if recipe['name'].lower() == name.lower():
                return jsonify(recipe)
        
        return jsonify({'message': 'Recipe not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
