from flask import Flask, render_template
from database import products_collection, init_db

app = Flask(__name__)

# Initialize database
init_db()

@app.route('/')
def home():
    try:
        products = list(products_collection.find()) if products_collection else []
        return render_template("index.html", products=products)
    except Exception as e:
        print(f"Error fetching products: {str(e)}")
        return render_template("index.html", products=[])

@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html", products=[]), 404

if __name__ == "__main__":
    app.run(debug=True)

