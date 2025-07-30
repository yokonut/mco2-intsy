from flask import Flask, render_template, request, jsonify
from interface import family  # Your Prolog instance and logic

app = Flask(__name__)

# Home route (optional, for index.html)
@app.route("/", methods=["GET", "POST"])
def home():
    result = ""
    if request.method == "POST":
        query = request.form["query"]
        try:
            output = list(family.query(query))
            result = output if output else "No match found"
        except Exception as e:
            result = f"Error: {e}"
    return render_template("index.html", result=result)

# Show ChatBunny frontend
@app.route("/chat", methods=["GET"])
def show_chat():
    return render_template("chat.html")

# Handle chatbot input and respond
@app.route("/chat", methods=["POST"])
def handle_chat():
    user_input = request.form.get("query", "")
    try:
        output = list(family.query(user_input))
        response = "True" if output else "False"
    except Exception as e:
        response = "Bunny not intelligent enough for that."
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
