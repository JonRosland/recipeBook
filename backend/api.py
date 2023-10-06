from flask import Flask, request, jsonify
from server import addRecipe, getRecipe, updateRecipe, deleteRecipe, searchRecipe, getRecipes
import json

app = Flask(__name__)

@app.route('/recipes/<id>', methods=['PUT'])
def apiPUT(id):
    data = request.json
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    response = updateRecipe(id, data)
    return jsonify(response), 200

@app.route('/recipes/search/<search>', methods=['GET'])
def apiSearch(search):
    search_dict = json.loads(search)
    recipe = searchRecipe(search_dict)
    if recipe:
        return jsonify(recipe), 200
    else:
        return jsonify({"message": "Recipe not found"}), 404

@app.route('/recipes/<id>', methods=['DELETE'])
def apiDELETE(id):
    response = deleteRecipe(id)
    return jsonify(response), 200

@app.route('/recipes/', methods=['POST'])
def apiPOST():
    data = request.json
    if not data:
        return jsonify({"message": "No input data provided"}), 400
    recipe_id = addRecipe(data)
    return jsonify({"recipe_id": str(recipe_id.inserted_id)}), 201

@app.route('/recipes/<id>', methods=['GET'])
def apiGET(id):
    recipe = getRecipe(id)
    if recipe:
        return jsonify(recipe), 200
    else:
        return jsonify({"message": "Recipe not found"}), 404
    
@app.route('/recipes/', methods=['GET'])
def getAllRecipes():
    recipes = getRecipes()
    return jsonify(list(recipes)), 200