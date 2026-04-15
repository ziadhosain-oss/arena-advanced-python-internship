from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ========== DATABASE MODELS ==========
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    district = db.Column(db.String(50), nullable=False)
    upazila = db.Column(db.String(50), nullable=False)
    full_address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='pending')
    total_amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)

# ========== ADMIN AUTH DECORATOR ==========
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'warning')
            return redirect(url_for('login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin:
            flash('Admin access required', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ========== ROUTES ==========
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            if user.is_admin:
                return redirect(url_for('admin_orders'))
            else:
                flash('User access only', 'warning')
                return redirect(url_for('login'))
        flash('Invalid credentials', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

# ========== ADMIN ROUTES ==========
@app.route('/admin/orders')
@admin_required
def admin_orders():
    # Get filter parameters
    status_filter = request.args.get('status', '')
    search = request.args.get('search', '')
    
    query = Order.query
    
    if status_filter:
        query = query.filter(Order.status == status_filter)
    
    if search:
        query = query.filter(
            db.or_(
                Order.order_number.ilike(f'%{search}%'),
                Order.customer_name.ilike(f'%{search}%'),
                Order.email.ilike(f'%{search}%'),
                Order.phone.ilike(f'%{search}%')
            )
        )
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    # Status counts for badges
    status_counts = {
        'pending': Order.query.filter_by(status='pending').count(),
        'processing': Order.query.filter_by(status='processing').count(),
        'shipped': Order.query.filter_by(status='shipped').count(),
        'delivered': Order.query.filter_by(status='delivered').count(),
        'cancelled': Order.query.filter_by(status='cancelled').count()
    }
    
    return render_template('admin_orders.html', 
                         orders=orders, 
                         status_filter=status_filter,
                         search=search,
                         status_counts=status_counts)

@app.route('/admin/orders/<int:order_id>')
@admin_required
def admin_order_details(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_details.html', order=order)

@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    
    if new_status in valid_statuses:
        order.status = new_status
        db.session.commit()
        flash(f'Order #{order.order_number} status updated to {new_status}', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('admin_order_details', order_id=order_id))

# ========== SAMPLE DATA ==========
def create_sample_orders():
    if Order.query.count() == 0:
        sample_orders = [
            {
                'order_number': 'ORD-001',
                'customer_name': 'John Doe',
                'email': 'john@example.com',
                'phone': '01712345678',
                'address': 'House 12, Road 5',
                'district': 'Dhaka',
                'upazila': 'Gulshan',
                'full_address': 'House 12, Road 5, Gulshan, Dhaka-1212',
                'status': 'pending',
                'total_amount': 1250.00,
                'items': [
                    {'product_name': 'Wireless Mouse', 'quantity': 2, 'price': 250.00, 'subtotal': 500.00},
                    {'product_name': 'Keyboard', 'quantity': 1, 'price': 750.00, 'subtotal': 750.00}
                ]
            },
            {
                'order_number': 'ORD-002',
                'customer_name': 'Jane Smith',
                'email': 'jane@example.com',
                'phone': '01812345678',
                'address': 'Block C, Road 10',
                'district': 'Chittagong',
                'upazila': 'Khulshi',
                'full_address': 'Block C, Road 10, Khulshi, Chittagong',
                'status': 'processing',
                'total_amount': 3500.00,
                'items': [
                    {'product_name': 'Laptop Bag', 'quantity': 1, 'price': 1500.00, 'subtotal': 1500.00},
                    {'product_name': 'USB Drive', 'quantity': 4, 'price': 500.00, 'subtotal': 2000.00}
                ]
            },
            {
                'order_number': 'ORD-003',
                'customer_name': 'Mike Johnson',
                'email': 'mike@example.com',
                'phone': '01912345678',
                'address': '15/A, Main Street',
                'district': 'Rajshahi',
                'upazila': 'Boalia',
                'full_address': '15/A, Main Street, Boalia, Rajshahi',
                'status': 'delivered',
                'total_amount': 890.00,
                'items': [
                    {'product_name': 'Headphones', 'quantity': 1, 'price': 890.00, 'subtotal': 890.00}
                ]
            }
        ]
        
        for order_data in sample_orders:
            order = Order(
                order_number=order_data['order_number'],
                customer_name=order_data['customer_name'],
                email=order_data['email'],
                phone=order_data['phone'],
                address=order_data['address'],
                district=order_data['district'],
                upazila=order_data['upazila'],
                full_address=order_data['full_address'],
                status=order_data['status'],
                total_amount=order_data['total_amount']
            )
            db.session.add(order)
            db.session.flush()
            
            for item_data in order_data['items']:
                item = OrderItem(
                    product_name=item_data['product_name'],
                    quantity=item_data['quantity'],
                    price=item_data['price'],
                    subtotal=item_data['subtotal'],
                    order_id=order.id
                )
                db.session.add(item)
        
        db.session.commit()
        print("✓ Sample orders created!")
        print(f"  - {len(sample_orders)} orders added to database")

# ========== INITIALIZE DATABASE ==========
with app.app_context():
    # Create database tables
    db.create_all()
    print("✓ Database tables created")
    
    # Create admin user if not exists
    if not User.query.filter_by(email='admin@example.com').first():
        admin = User(
            email='admin@example.com',
            password=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print("✓ Admin user created")
        print("  Email: admin@example.com")
        print("  Password: admin123")
    else:
        print("✓ Admin user already exists")
    
    # Create sample orders
    create_sample_orders()
    
    # Print summary
    print("\n" + "="*50)
    print("APPLICATION READY!")
    print("="*50)
    print(f"Admin email: admin@example.com")
    print(f"Admin password: admin123")
    print(f"Total orders: {Order.query.count()}")
    print(f"Total users: {User.query.count()}")
    print("="*50 + "\n")

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Access the application at: http://localhost:5000")
    print("Press CTRL+C to stop the server\n")
    app.run(debug=True)