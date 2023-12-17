from . import db
from flask_login import UserMixin
from sqlalchemy import LargeBinary


#User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    recipes = db.relationship('Recipe')

#Recipe Model
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_name = db.Column(db.String(255), nullable=False)
    recipe_description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    recipe_image_url = db.Column(db.String(255), nullable=False)