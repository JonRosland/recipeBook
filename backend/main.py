from api import app
from server import addRecipe, connectToDB, dump_recipes_as_json
import json   

if __name__ == "__main__":  
    
    app.run(debug=True)
