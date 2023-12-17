from flask import Blueprint, render_template, request, flash, send_from_directory, url_for
from flask_login import login_required, current_user
from .models import Recipe
from werkzeug.utils import secure_filename
from . import db
from flask import jsonify, json
from sqlalchemy import or_
import os

views = Blueprint("views", __name__)

@views.route('/')
@login_required
def Home():
    all_recipes = db.session.query(Recipe).order_by(Recipe.id.desc()).limit(5).all()
    return render_template("Home.html", user=current_user, recipes=all_recipes)


@views.route('/uploads', methods=['GET', 'POST'])
@login_required
def submit_form():
    if request.method == "POST":
        recipe_name = request.form.get('name')
        description = request.form.get("description")
        ingredients = request.form.get("ingredients")
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join("website/static/uploads", filename))

        if len(recipe_name) < 2:
            flash("Recipe Name is too short!")
        elif len(description) < 5:
            flash("Description is too short!")
        elif len(ingredients) < 5 :
            flash("list of ingredients are too short!")
        elif file is None:
            flash("Please attch a photo!")
        else:
            new_recipe = Recipe(user_id = current_user.id, recipe_name=recipe_name, recipe_description=description, ingredients=ingredients, recipe_image_url=filename)
            db.session.add(new_recipe)
            db.session.commit()
            flash("Recipe is added!")
    return render_template('submit.html', user=current_user)


@views.route('/about')
@login_required
def about():
    return render_template('about.html', user=current_user)

@views.route('/yourrecipe')
@login_required
def your_recipe():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template('your_recipe.html', user=current_user, recipes=recipes)

@views.route('/static/uploads/<filename>')
def uploaded_file(filename):
    path = 'static/uploads'
    return send_from_directory(path, filename)

@views.route('/explore')
@login_required
def explore():
    all_recipes = db.session.query(Recipe).order_by(Recipe.id.desc()).all()
    return render_template('explore.html', user=current_user, recipes=all_recipes)

@views.route('/yourrecipe/<int:id>')
@login_required
def recipe_details(id):
    recipe = db.session.query(Recipe).get(id)
    # print(recipe)
    return render_template('recipe_details.html',user=current_user, recipe=recipe)

@views.route('/search')
def search():
    query = request.args.get('query', '')
    user_specific_results = Recipe.query.filter(
            (Recipe.user_id == current_user.id) &
            or_(
                Recipe.recipe_name.ilike(f"%{query}%"),
                Recipe.recipe_description.ilike(f"%{query}%"),
                Recipe.ingredients.ilike(f"%{query}%")
            )
        ).all()
    
    # print("user_specific - ", user_specific_results)

    results_json = [
        {'name': recipe.recipe_name, 
        'url': url_for('views.recipe_details', id=recipe.id), 
        'img_url': url_for('views.uploaded_file', filename=recipe.recipe_image_url)
        }
        for recipe in user_specific_results]
    
    return jsonify(results_json)


@views.route('/search_all')
def search_all():
    query = request.args.get('query', '')
    all_results = Recipe.query.filter(
            or_(
                Recipe.recipe_name.ilike(f"%{query}%"),
                Recipe.recipe_description.ilike(f"%{query}%"),
                Recipe.ingredients.ilike(f"%{query}%")
            )
        ).all()

    # print("all results - ", all_results)

    results_json = [
        {'name': recipe.recipe_name, 
        'url': url_for('views.recipe_details', id=recipe.id), 
        'img_url': url_for('views.uploaded_file', filename=recipe.recipe_image_url)
        }
        for recipe in all_results]
    
    return jsonify(results_json)


@views.route('/delete-recipe', methods=["POST"])
def delete_recipe():
    recipe = json.loads(request.data)
    print(recipe)
    recipeId = recipe['recipeId']
    print(recipeId)
    recipe = Recipe.query.get(recipeId)
    print(recipe)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()

    return jsonify({})

@views.route('/editrecipe/<int:id>', methods=["POST", "GET"])
def edit_recipe(id):
    recipe = Recipe()
    to_update = Recipe.query.get_or_404(id)
    if request.method == "POST":
        to_update.recipe_name = request.form['name']
        to_update.recipe_description = request.form['description']
        to_update.ingredients = request.form['ingredients']
        if 'file' in request.files:
            file = request.files['file']
            if file and file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join("website/static/uploads", filename))
                to_update.recipe_image_url = filename
        try:
            db.session.commit()
            print("updated!")
            return render_template("editrecipe.html",
            recipe = recipe,
            to_update = to_update, user=current_user)
        except:
            print("Something went wrong!")
            return render_template("editrecipe.html",
            recipe = recipe,
            to_update = to_update)
    else:
        print("Something went wrong")
        return render_template("editrecipe.html",
            recipe = recipe,
            to_update = to_update,
            user = current_user)











