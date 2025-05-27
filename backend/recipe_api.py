from flask import Blueprint, jsonify, request
from utils.sheets import get_recipes
import traceback

recipe_bp = Blueprint('recipe_bp', __name__)

@recipe_bp.route('/recipes', methods=['GET'])
def get_all_recipes():
    """Get all recipes from Google Sheets"""
    try:
        print("Blueprint: Fetching all recipes...")
        recipes = get_recipes()
        print(f"Blueprint: Found {len(recipes)} recipes")
        return jsonify(recipes)
    except Exception as e:
        print(f"Blueprint: Error fetching recipes: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@recipe_bp.route('/recipes/<string:name>', methods=['GET'])
def get_recipe(name):
    """Get a specific recipe by name"""
    try:
        print(f"Blueprint: Fetching recipe: {name}")
        recipes = get_recipes()
        for recipe in recipes:
            if recipe['name'].lower() == name.lower():
                print(f"Blueprint: Found recipe: {recipe['name']}")
                return jsonify(recipe)
        
        print(f"Blueprint: Recipe not found: {name}")
        return jsonify({'message': 'Recipe not found'}), 404
    except Exception as e:
        print(f"Blueprint: Error fetching recipe {name}: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500
