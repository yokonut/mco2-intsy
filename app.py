from flask import Flask, request, render_template, jsonify
from interface import handle_user_input

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

#chat
@app.route('/chat', methods=['GET'])
def show_chat():
    return render_template('chat.html')

# process
@app.route('/chat', methods=['POST'])
def handle_chat():
    user_input = request.form.get('query', '')
    if not user_input.strip():
        return jsonify({'response': '🤔 Please enter a question or statement.'})
    try:
        response = handle_user_input(user_input)
        return jsonify({'response': str(response)})
    except Exception as e:
        return jsonify({'response': f'❌ Bunny had a hiccup. Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
