from flask import Flask, request, render_template, jsonify
from interface import handle_user_input

app = Flask(__name__)

# In-memory conversation log (for demo purposes)
conversation_history = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['GET'])
def show_chat():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def handle_chat():
    user_input = request.form.get('query', '').strip()
    if not user_input:
        return jsonify({'response': '🤔 Please enter a question or statement.', 'log': conversation_history})
    
    try:
        response = str(handle_user_input(user_input))
    except Exception as e:
        response = f'❌ Bunny had a hiccup. Error: {str(e)}'

    # Append to conversation history
    conversation_history.append({'user': user_input, 'bot': response})
    
    return jsonify({'response': response, 'log': conversation_history})

if __name__ == '__main__':
    app.run(debug=True)
