from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/echo/<text>")
def echo_text(text):
    return f"<p>You said: {text}</p>"

@app.route("/post-only", methods=["POST"])
def post_only():
    data = request.form.get("data", "No data received")
    return f"<p>POST request received with data: {data}</p>"

@app.route("/show-template")
def show_template():
    return render_template("hello.html", name="Ziad")

if __name__ == "__main__":
    app.run(debug=True, port=8888)