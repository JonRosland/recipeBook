from pymongo import MongoClient
from bson.objectid import ObjectId
import json

def connectToDB():
    #client = MongoClient("mongodb://root:root@mongo:27017/")
    client = MongoClient('10.0.0.10', 27017, username='root', password='root')
    #client = MongoClient('mongo', 27017, username='root', password='root')
    #client.server_info()
    db = client["RecipeDB"]
    db_recipe = db["Food"]

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
    recipes_cursor = db_recipe.find()
    recipes_list = list(recipes_cursor)
    client.close()
    for recipe in recipes_list:
        recipe['_id'] = str(recipe['_id'])
    return recipes_list

def deleteRecipe(id):
    db_recipe, client = connectToDB()
    response = db_recipe.delete_one({"_id": ObjectId(id)})
    client.close()
    return {"message": "Recipe deleted"} if response.deleted_count else {"message": "Recipe not found"}

def updateRecipe(id, data):
    db_recipe, client = connectToDB()
    data.pop('_id')
    response = db_recipe.update_one({"_id": ObjectId(id)}, {'$set': data})
    client.close()
    return {"message": "Recipe updated"} if response.modified_count else {"message": "Recipe not found"}

def addRecipe(recipe):
    print('in add recipe')
    db_recipe, client = connectToDB()
    print('after connected to db')
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

def dump_recipes_as_json():
    db_recipe, client = connectToDB()
    recipes = db_recipe.find({})

    for recipe in recipes:
        # Convert ObjectId to string
        recipe['_id'] = str(recipe['_id'])
        
        # Dump the recipe as a JSON file
        with open(f"recipes/{recipe['_id']}.json", 'w') as file:
            json.dump(recipe, file, indent=4)