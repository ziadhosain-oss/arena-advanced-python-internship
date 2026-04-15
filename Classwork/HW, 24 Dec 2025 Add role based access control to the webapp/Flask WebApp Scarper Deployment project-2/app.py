from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import db, init_db, products_collection, users_collection, User
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from scraper import scrape_product
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = 'adsadasdasdasd'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

init_db()

@login_manager.user_loader
def load_user(user_id):
    user_data = users_collection.find_one({'_id': ObjectId(user_id)})
    return User(user_data) if user_data else None

# --- Auth Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = users_collection.find_one({"username": username})
        if user_data and user_data['password'] == password:
            user_obj = User(user_data)
            login_user(user_obj)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('admin_view'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('public_view'))

# --- Admin Routes ---
@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_view():
    results = []
    if request.method == 'POST':
        query = request.form.get('query')
        results = scrape_product(query)
    return render_template('admin.html', results=results)

@app.route('/admin/add_user', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users_collection.find_one({'username': username}):
            flash('Username already exists.', 'danger')
            return redirect(url_for('add_user'))
        else:
            users_collection.insert_one({'username': username, 'password': password})
            flash('User added successfully.', 'success')
            return redirect(url_for('add_user'))
    return render_template('add_user.html')

@app.route('/admin/list_user')
@login_required
def list_user():
    users = list(users_collection.find())
    return render_template('list_user.html', users=users)

@app.route('/delete_user', methods=['POST'])
@login_required
def delete_user():
    data = request.get_json()
    username = data.get('username')
    result = users_collection.delete_one({'username': username})
    if result.deleted_count == 1:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error'}), 500

@app.route('/save', methods=['POST'])
@login_required
def save_product():
    # json
    data = request.get_json()
    product_data = {
        'name': data['name'],
        'price': data['price'],
        'img_url': data['img_url'],
        'product_url': data['product_url']
    }
    result = products_collection.insert_one(product_data)
    # flash('Product saved successfully.', 'success')
    # return redirect(url_for('admin_view'))
    if result.inserted_id:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error'}), 500

@app.route('/delete/<product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    product_id = ObjectId(product_id)
    result = products_collection.delete_one({'_id': product_id})
    if result.deleted_count == 1:
        return jsonify({'status': 'success'}), 200
    else:
        return jsonify({'status': 'error'}), 500
    return redirect(url_for('admin_view'))

# --- Public Routes ---
@app.route('/')
def public_view():
    products = list(products_collection.find())
    return render_template('public.html', products=products)


if __name__ == '__main__':
    app.run(debug=True, port=8010)
