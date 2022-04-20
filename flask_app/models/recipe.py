from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db_name = 'cook_book'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.instruction = db_data['instruction']
        self.difficulty = db_data['difficulty']
        self.vote = db_data['vote']
        self.ingredients = db_data['ingredients']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at'] 
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instruction, ingredients, difficulty, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(ingredients)s, %(difficulty)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db_name).query_db(query)
        all_recipes = []
        for row in results:
            all_recipes.append(cls(row))
        return all_recipes

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, ingredients=%(ingredients)s, difficulty=%(difficulty)s,updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def vote(cls,data):
        query = "UPDATE recipes SET vote = vote + 1 WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 1:
            is_valid = False
            flash("Name is required","recipe")
        if len(recipe['filling']) < 1:
            is_valid = False
            flash("Filling is required","recipe")
        if len(recipe['crust']) < 1:
            is_valid = False
            flash("Crust is required","recipe")
        return is_valid