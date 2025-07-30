from flask import Flask, render_template, request, jsonify
from interface import family, handle_user_input  # Updated import

app = Flask(__name__)

# Home route (optional, for index.html)
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        if query.strip():
            try:
                result = handle_user_input(query)
            except Exception as e:
                result = f"❌ Error: {str(e)}"
        else:
            result = "🤔 Please enter a question or statement."
    return render_template("index.html", result=result)

# Show ChatBunny frontend
@app.route("/chat", methods=["GET"])
def show_chat():
    return render_template("chat.html")

# Handle chatbot input and respond
@app.route("/chat", methods=["POST"])
def handle_chat():
    user_input = request.form.get("query", "")
    if not user_input.strip():
        return jsonify({"response": "🤔 Please enter a question or statement."})
    
    try:
        response = handle_user_input(user_input)
        # Ensure response is a string
        if response is None:
            response = "🤔 I didn't understand that. Please try again."
        return jsonify({"response": str(response)})
    except Exception as e:
        return jsonify({"response": f"❌ Bunny not intelligent enough for that. Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)