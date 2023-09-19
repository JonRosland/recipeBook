from pymongo import MongoClient
from recipeClass import Recipe, Ingredient
from bson.objectid import ObjectId


def connectToDB():
    #client = MongoClient("mongodb://root:root@localhost:27017")
    client = MongoClient('localhost', 27017, username='root', password='root')
    client.server_info()

    db = client["coockbookdb"]
    recipes_col = db["recipes"]
    return recipes_col, client

def getRecipe(id):
    db, client = connectToDB()
    recipe = db.find_one({"_id": ObjectId(id)})
    client.close()
    return recipe

def deleteRecipe(id):
    db, client = connectToDB()
    response = db.delete_one({"_id": ObjectId(id)})
    client.close()
    return {"message": "Recipe deleted"} if response.deleted_count else {"message": "Recipe not found"}

def updateRecipe(id, data):
    db, client = connectToDB()
    response = db.update_one({"_id": ObjectId(id)}, {'$set': data})
    client.close()
    return {"message": "Recipe updated"} if response.modified_count else {"message": "Recipe not found"}

def addRecipe(recipe):
    db, client = connectToDB()
    recipe_id = db.insert_one(recipe)
    client.close()
    return recipe_id
