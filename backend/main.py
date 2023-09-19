from api import app
from server import connectToDB
import json

if __name__ == "__main__":  
    
#    db = connectToDB()
#    with open('/home/jonro/recipeBook/backend/recipeEx.json', 'r') as file:
#        json_data = json.load(file)
#    x = db.insert_one(json_data)

    app.run(debug=True)
