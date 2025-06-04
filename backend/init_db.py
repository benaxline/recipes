# backend/init_db.py

import os
from app import app, db
from models import Recipe

# Path to your sqlite file (relative to this script)
DB_PATH = os.path.join(os.path.dirname(__file__), 'recipes.db')

if __name__ == '__main__':
    # 1) remove the old DB file so we start totally fresh
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print("Removed old recipes.db")

    with app.app_context():
        # 2) explicitly create just the Recipe table
        Recipe.__table__.create(bind=db.engine)
        print("Created 'recipes' table")