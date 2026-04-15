from flask import Flask, jsonify
from scraper import scrape_startech

app = Flask(__name__)

@app.route('/search/<query>')
def search(query):
    products = scrape_startech(query)
    return jsonify({'products': products})

if __name__ == '__main__':
    app.run(port=5000)