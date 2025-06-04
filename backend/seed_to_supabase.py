# backend/seed_to_supabase.py

import os
import traceback
from dotenv import load_dotenv
from supabase import create_client, Client

# Make sure your utils/sheets.py is importable:
import sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)
from utils.sheets import get_recipes

# 1) Load environment variables from .env (if you have one)
load_dotenv()

# 2) Initialize Supabase client
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError("You must set SUPABASE_URL and SUPABASE_KEY in your environment")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def seed():
    """
    Pulls all recipes from Google Sheets (via get_recipes())
    and inserts each row into the Supabase 'recipes' table,
    skipping any duplicate names.
    """
    added = 0
    try:
        sheet_data = get_recipes()  # returns a list of dicts with keys: name, author, type, ingredients, instructions
    except Exception as e:
        print("Error reading from Google Sheets:", e)
        return

    for row in sheet_data:
        name = row.get('name')
        if not name:
            continue  # skip rows without a name

        # 3) Check if a recipe with the same name already exists in Supabase
        try:
            existing = (
                supabase
                .from_('Recipes')
                .select('id')
                .eq('name', name)
                .limit(1)
                .execute()
            )
        except Exception as e:
            print(f"Error querying Supabase for existing '{name}':", e)
            continue

        if existing.data:
            # Already have a row with this name; skip it
            continue

        # Build the record payload. Supabase expects text fields for ingredients/instructions:
        payload = {
            'name': name,
            'author': row.get('author'),
            'category': row.get('type'),
            'ingredients': '\n'.join(row.get('ingredients', [])),
            'instructions': '\n'.join(row.get('instructions', []))
        }

        # 4) Insert into Supabase
        try:
            result = supabase.from_('recipes').insert(payload).execute()
            if result.error:
                print(f"  • Error inserting '{name}':", result.error)
            else:
                added += 1
                print(f"  • Inserted '{name}' (id={result.data[0]['id']})")
        except Exception as e:
            print(f"  • Exception inserting '{name}':", e)

    print(f"\nSeeding complete. Added {added} new recipes to Supabase.")

if __name__ == '__main__':
    seed()
