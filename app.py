from flask import Flask, request, render_template, jsonify
from interface import handle_user_input

app = Flask(__name__)

@app.route('/')
def show_chat():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['query']
    response = handle_user_input(user_input)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
