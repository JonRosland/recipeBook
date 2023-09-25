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

def searchRecipe(search):
    db_recipe, client = connectToDB()
    print(search)
    recipes_cursor = db_recipe.find({"category":"dinner"})
    print(recipes_cursor)
    recipes_list = list(recipes_cursor)
    print(recipes_list)
    client.close()
    return recipes_list

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
