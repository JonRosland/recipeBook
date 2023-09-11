from pymongo import MongoClient
from recipeClass import Recipe, Ingredient
import json

def load_recipe_from_json_file(file_path):
    with open(file_path, 'r') as file:
        json_data = json.load(file)
        return Recipe.from_json(json_data)


if __name__ == "__main__":   
  
    client = MongoClient("mongodb://root:root@localhost:27017")
    client.server_info()

    db = client["coockbookdb"]
    recipes_col = db["recipes"]


    x = recipes_col.insert_one(meatballs)

    print(client.list_database_names())


