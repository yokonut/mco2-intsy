from flask import Flask, render_template, request
from relationships import assertz
from interface import family

app = Flask(__name__)

@app.route("/chat")
def chat():
    return render_template("chat.html")


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

if __name__ == "__main__":
    app.run(debug=True)
