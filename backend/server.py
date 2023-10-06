from pymongo import MongoClient
from recipeClass import Recipe, Ingredient
from bson.objectid import ObjectId
import json
from flask import jsonify


def connectToDB():
    #client = MongoClient("mongodb://root:root@localhost:27017")
    client = MongoClient('localhost', 27017, username='root', password='root')
    client.server_info()

    db = client["coockbookdb"]
    db_recipe = db["recipes"]
    return db_recipe, client

def getRecipe(id):
    db_recipe, client = connectToDB()
    recipe = db_recipe.find_one({"_id": ObjectId(id)})
    client.close()
    if recipe:
        recipe['_id'] = str(recipe['_id'])
    return recipe

def getRecipes():
    db_recipe, client = connectToDB()
    recipes = db_recipe.find({})
    client.close()
    for recipe in recipes:
        recipe['_id'] = str(recipe['_id'])
    return recipes

def deleteRecipe(id):
    db_recipe, client = connectToDB()
    response = db_recipe.delete_one({"_id": ObjectId(id)})
    client.close()
    return {"message": "Recipe deleted"} if response.deleted_count else {"message": "Recipe not found"}

def updateRecipe(id, data):
    db_recipe, client = connectToDB()
    response = db_recipe.update_one({"_id": ObjectId(id)}, {'$set': data})
    client.close()
    return {"message": "Recipe updated"} if response.modified_count else {"message": "Recipe not found"}

def addRecipe(recipe):
    db_recipe, client = connectToDB()
    recipe_id = db_recipe.insert_one(recipe)
    client.close()
    return recipe_id

def searchRecipe(search):
    db_recipe, client = connectToDB()
    recipes_cursor = db_recipe.find(search)
    recipes_list = list(recipes_cursor)
    client.close()
    for recipe in recipes_list:
        recipe['_id'] = str(recipe['_id'])
    return recipes_list

folder_path = "../recipes"
def dump_recipes_as_json():
    db_recipe, client = connectToDB()
    recipes = db_recipe.find({})

    for recipe in recipes:
        # Convert ObjectId to string
        recipe['_id'] = str(recipe['_id'])
        
        # Dump the recipe as a JSON file
        with open(f"recipes/{recipe['_id']}.json", 'w') as file:
            json.dump(recipe, file, indent=4)