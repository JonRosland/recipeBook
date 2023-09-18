from pymongo import MongoClient
from recipeClass import Recipe, Ingredient
from api import app
import json
import requests

def connectToDB():
    #client = MongoClient("mongodb://root:root@localhost:27017")
    client = MongoClient('localhost', 27017, username='root', password='root')
    client.server_info()

    db = client["coockbookdb"]
    recipes_col = db["recipes"]
    return recipes_col



if __name__ == "__main__":   
    db = connectToDB()


    with open('/home/jonro/recipeBook/backend/recipeEx.json', 'r') as file:
        json_data = json.load(file)


    x = db.insert_one(json_data)

    print(x.inserted_id)

    app.run(debug=True)
