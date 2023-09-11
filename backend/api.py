from flask import Flask, request, jsonify

app = Flask(__name__)

messages = []

@app.route('/recipes', methods=['GET', 'POST'])

def handle_messages():
    if request.method == 'GET':
        return jsonify(messages)
    
    elif request.method == 'POST':
        new_message = request.get_json()
        messages.append(new_message)
        print(new_message)
        return jsonify(new_message), 201

if __name__ == '__main__':
    app.run(debug=True)
