from flask import Flask, request, jsonify
from server import connectToDB

app = Flask(__name__)


@app.route('/recipes', methods=['POST', 'GET'])
def addRecipe():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify(data), 201
    elif request.method == 'GET':
        data = request.get_json()
        return jsonify(data), 201
    else:
        return jsonify({'data': 'Hello World'})

def getRecipes():
    return jsonify({'data': 'Hello World'})
    
@app.route('/recipes/<id>', methods=['GET', 'PUT', 'DELETE'])
def getRecipe(id):
    if request.method == 'GET':
        return jsonify({'data': 'Hello World'})
    elif request.method == 'PUT':
        return jsonify({'data': 'Hello World'})
    elif request.method == 'DELETE':
        return jsonify({'data': 'Hello World'})
    else:
        return jsonify({'data': 'Hello World'})

