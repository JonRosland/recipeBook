from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/recipes', methods=['GET', 'POST'])

#create a simple api to get a post request and return a json object
def recipes():
    if request.method == 'POST':
        data = request.get_json()
        return jsonify({'data': data}), 201
    else:
        return jsonify({'data': 'Hello World'})



if __name__ == '__main__':
    app.run(debug=True)

