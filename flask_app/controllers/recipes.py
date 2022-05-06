from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User

@app.route('/new/recipe')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_recipe.html', user=User.get_by_id(data))

@app.route('/create/recipe',methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instruction": request.form["instruction"],
        "ingredients": request.form["ingredients"],
        "difficulty": request.form["difficulty"],
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/edit/recipe/<int:id>')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    return render_template("edit_recipe.html",recipe=Recipe.get_by_id(data))

@app.route('/update/recipe',methods=['POST'])
def update_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":request.form["id"],
        "name": request.form["name"],
        "description": request.form["description"],
        "instruction": request.form["instruction"],
        "ingredients": request.form["ingredients"],
        "difficulty": request.form["difficulty"],
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/show/<int:id>')
def show_recipe(id):
    data = {
        "id":id
    }

    return render_template("detail_recipe.html",recipe=Recipe.get_by_id(data),users=User.get_all())

@app.route('/delete/recipe/<int:id>')
def delete_recipe(id):
    
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.delete(data)
    return redirect('/dashboard')

@app.route('/')
def homepage():
    return render_template("homepage.html", recipes=Recipe.get_all(), users=User.get_all())

@app.route('/search', methods=['POST', 'GET'])
def search():
    data = {
        "keyword": request.form["keyword"],  
    }
    return render_template("homepage.html", keyword = data["keyword"], recipes=Recipe.get_all_contains(data), users=User.get_all())

@app.route('/vote/<int:id>')
def vote(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.vote(data)
    return render_template("homepage.html", recipes=Recipe.get_all(), users =User.get_all())