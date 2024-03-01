from api import app
#from server import addRecipe, connectToDB, dump_recipes_as_json
#import json   

if __name__ == "__main__":  
    #db, client = connectToDB()
    #with open('/home/ubuntu/recipeBook/backend/recipeEx.json', 'r') as file:
    #    json_data = json.load(file)
    #x = db.insert_one(json_data)
    app.run(debug=True, port=4000, host='0.0.0.0')
