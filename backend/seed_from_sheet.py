# backend/seed_from_sheet.py

import os
from app import app, db
from models import Recipe
from utils.sheets import get_recipes
from sqlalchemy.orm import sessionmaker

db.app = app


def seed():
    """
    Seed the database with recipes from Google Sheets.
    
    Returns:
        int: Number of recipes added to the database.
    """
    added = 0
    with app.app_context():
        
        sheet_data = get_recipes()

        for s in sheet_data:
            name = s.get('name')
            if not name:
                continue

            if db.session.query(Recipe).filter_by(name=name).first():
                continue

            recipe = Recipe(
                name=s['name'],
                author=s['author'],
                type=s['type'],
                ingredients='\n'.join(s['ingredients']),
                instructions='\n'.join(s['instructions'])
            )
            db.session.add(recipe)
            added += 1

        db.session.commit()
        print(f'{added} recipes added to the database.')

if __name__ == '__main__':
    seed()
