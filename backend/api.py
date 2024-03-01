from flask import Flask, request, jsonify
from server import addRecipe, getRecipe, updateRecipe, deleteRecipe, searchRecipe, getRecipes
import json
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/api/<id>', methods=['PUT'])
def apiPUT(id):
    data = request.json
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    response = updateRecipe(id, data)
    return jsonify(response), 200

@app.route('/api/search/<search>', methods=['GET'])
def apiSearch(search):
    search_dict = json.loads(search)
    recipe = searchRecipe(search_dict)
    if recipe:
        return jsonify(recipe), 200
    else:
        return jsonify({"message": "Recipe not found"}), 404

# @app.route('/api/<id>', methods=['DELETE'])
# def apiDELETE(id):
#     response = deleteRecipe(id)
#     return jsonify(response), 200

@app.route('/api/newRecipe', methods=['POST'])
def apiPOST():
    print('in POST')
    data = request.json
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    recipe_id = addRecipe(data)
    return jsonify({"recipe_id": str(recipe_id.inserted_id)}), 201

@app.route('/api/test', methods=['GET'])
def apitest():
    return jsonify({'Connection':'success'}), 200

@app.route('/api/<id>', methods=['GET'])
def apiGET(id):
    recipe = getRecipe(id)
    if recipe:
        return jsonify(recipe), 200
    else:
        return 0, 404
    
@app.route('/api/', methods=['GET'])
def getAllRecipes():
    recipes = getRecipes()
    return jsonify(list(recipes)), 200