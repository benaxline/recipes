from backend.app import db
from datetime import datetime
from sqlalchemy import func

class Recipe(db.Model):
    """
    Recipe model for SQLAlchemy.

    Attributes:
        id (int): Primary key.
        name (str): Name of the recipe.
        author (str): Author of the recipe.
        type (str): Type of the recipe (e.g., 'Dessert', 'Main Course').
        ingredients (str): Ingredients for the recipe.
        instructions (str): Instructions for the recipe.
        created_at (datetime): Date and time the recipe was created.
    """
    __tablename__ = 'recipes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(64), nullable=True)
    type = db.Column(db.String(64), nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=False)

    def to_dict(self):
        """
        Converts the Recipe object to a dictionary.

        Returns:
            dict: A dictionary representation of the Recipe object.
        """
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'type': self.type,
            'ingredients': self.ingredients.split('\n'),
            'instructions': self.instructions.split('\n'),
            'created_at': self.created_at.isoformat()
        }