# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Product, CartItem, Order, OrderItem, ProductStatus
from scraper import WebScraper
import uuid
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with app
db.init_app(app)
scraper = WebScraper()

# Helper function to get cart count
def get_cart_count():
    if 'cart_session_id' in session:
        return CartItem.query.filter_by(session_id=session['cart_session_id']).count()
    return 0

# Context processor for templates
@app.context_processor
def utility_processor():
    return {
        'cart_count': get_cart_count,
        'ProductStatus': ProductStatus
    }

# Initialize cart session
@app.before_request
def before_request():
    if 'cart_session_id' not in session:
        session['cart_session_id'] = str(uuid.uuid4())

# Create tables and add demo data
with app.app_context():
    db.create_all()
    
    # Add demo products if none exist
    if Product.query.count() == 0:
        demo_products = [
            Product(
                id=str(uuid.uuid4())[:12],
                name="Wireless Headphones",
                price=79.99,
                status=ProductStatus.IN_STOCK,
                original_price_text="$79.99",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="Smart Watch",
                price=199.99,
                status=ProductStatus.IN_STOCK,
                original_price_text="$199.99",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="Phone Case",
                price=None,
                status=ProductStatus.OUT_OF_STOCK,
                original_price_text="Out of Stock",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="New Gaming Console",
                price=None,
                status=ProductStatus.UPCOMING,
                original_price_text="Up Coming - Pre-order Soon",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="Laptop Stand",
                price=29.99,
                status=ProductStatus.IN_STOCK,
                original_price_text="$29.99",
                url="#"
            ),
        ]
        for product in demo_products:
            db.session.add(product)
        db.session.commit()
        print("✅ Added demo products to database")

# Home page - display all products
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Add demo products route
@app.route('/add_demo_products')
def add_demo_products():
    """Add demo products to show how the system works"""
    try:
        # Clear existing products (optional)
        # Product.query.delete()
        
        demo_products = [
            Product(
                id=str(uuid.uuid4())[:12],
                name="Wireless Headphones - Sony WH-1000XM4",
                price=79.99,
                status=ProductStatus.IN_STOCK,
                original_price_text="$79.99",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="Apple Watch Series 8",
                price=199.99,
                status=ProductStatus.IN_STOCK,
                original_price_text="$199.99",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="Premium Phone Case",
                price=None,
                status=ProductStatus.OUT_OF_STOCK,
                original_price_text="Out of Stock",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="PlayStation 6",
                price=None,
                status=ProductStatus.UPCOMING,
                original_price_text="Up Coming - Release Date TBA",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="Ergonomic Laptop Stand",
                price=29.99,
                status=ProductStatus.IN_STOCK,
                original_price_text="$29.99",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="Mechanical Keyboard",
                price=89.99,
                status=ProductStatus.IN_STOCK,
                original_price_text="$89.99",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="Gaming Mouse (Limited Edition)",
                price=None,
                status=ProductStatus.OUT_OF_STOCK,
                original_price_text="Sold Out",
                url="#"
            ),
            Product(
                id=str(uuid.uuid4())[:12],
                name="Next Gen VR Headset",
                price=None,
                status=ProductStatus.UPCOMING,
                original_price_text="Coming Soon - $499.99",
                url="#"
            ),
        ]
        
        for product in demo_products:
            existing = Product.query.filter_by(name=product.name).first()
            if not existing:
                db.session.add(product)
        
        db.session.commit()
        flash(f'Added {len(demo_products)} demo products to the database!', 'success')
    except Exception as e:
        flash(f'Error adding demo products: {str(e)}', 'error')
    
    return redirect(url_for('index'))

# Clear all products
@app.route('/clear_products')
def clear_products():
    """Clear all products (useful for testing)"""
    try:
        # First clear cart items
        CartItem.query.delete()
        # Then clear products
        Product.query.delete()
        db.session.commit()
        flash('All products have been cleared! Use "Add Demo Products" or "Scrape" to add new ones.', 'info')
    except Exception as e:
        flash(f'Error clearing products: {str(e)}', 'error')
    
    return redirect(url_for('index'))

# Scrape products (form submission) - IMPROVED VERSION
@app.route('/scrape', methods=['POST'])
def scrape_products():
    url = request.form.get('url')
    
    if not url:
        flash('URL is required', 'error')
        return redirect(url_for('index'))
    
    # List of known e-commerce sites that work well
    demo_sites = {
        'books.toscrape.com': 'http://books.toscrape.com',
        'scrapingclub.com': 'https://scrapingclub.com/exercise/list_basic/',
    }
    
    try:
        # Check if it's a test URL
        if 'test' in url.lower() or 'demo' in url.lower():
            # Add demo data instead of scraping
            return redirect(url_for('add_demo_products'))
        
        # Perform scraping
        scraped_products = perform_scraping(url)
        
        if not scraped_products:
            flash('No products found on this page. Try:\n'
                  '- Adding demo products using the button below\n'
                  '- Using a product listing URL (e.g., http://books.toscrape.com)\n'
                  '- Checking if the website has product items with prices', 'warning')
            return redirect(url_for('index'))
        
        products_created = 0
        products_updated = 0
        
        for product_data in scraped_products:
            product = Product.query.get(product_data.id)
            
            if product:
                # Update existing product
                old_status = product.status
                product.name = product_data.name
                product.price = product_data.price
                product.status = product_data.status
                product.original_price_text = product_data.original_price_text
                products_updated += 1
                
                # If product became unavailable, remove from carts
                if old_status == ProductStatus.IN_STOCK and product.status != ProductStatus.IN_STOCK:
                    CartItem.query.filter_by(product_id=product.id).delete()
            else:
                # Create new product
                product = Product(
                    id=product_data.id,
                    name=product_data.name,
                    price=product_data.price,
                    status=product_data.status,
                    original_price_text=product_data.original_price_text,
                    url=product_data.url
                )
                db.session.add(product)
                products_created += 1
        
        db.session.commit()
        
        flash(f'Success! Created {products_created} new products, updated {products_updated} products', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Scraping failed: {str(e)}. Try using the "Add Demo Products" button instead.', 'error')
    
    return redirect(url_for('index'))

# Add to cart (POST form)
@app.route('/cart/add/<product_id>', methods=['POST'])
def add_to_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    # Find product
    product = Product.query.get(product_id)
    if not product:
        flash('Product not found', 'error')
        return redirect(url_for('index'))
    
    # Check if product is available for purchase
    if not product.is_available_for_purchase():
        flash(f'❌ Cannot add to cart: "{product.name}" is {product.status.value.replace("_", " ")}', 'error')
        return redirect(url_for('index'))
    
    # Check if already in cart
    cart_item = CartItem.query.filter_by(
        product_id=product_id,
        session_id=session['cart_session_id']
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
        flash(f'✓ Updated {product.name} quantity in cart', 'info')
    else:
        cart_item = CartItem(
            product_id=product_id,
            session_id=session['cart_session_id'],
            quantity=quantity
        )
        db.session.add(cart_item)
        flash(f'✓ Added {product.name} to cart', 'success')
    
    try:
        cart_item.validate()
        db.session.commit()
    except ValueError as e:
        db.session.rollback()
        flash(str(e), 'error')
    
    return redirect(url_for('view_cart'))

# Update cart item quantity
@app.route('/cart/update/<int:cart_item_id>', methods=['POST'])
def update_cart_item(cart_item_id):
    quantity = int(request.form.get('quantity', 0))
    
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    # Verify cart belongs to current session
    if cart_item.session_id != session['cart_session_id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('view_cart'))
    
    if quantity <= 0:
        db.session.delete(cart_item)
        flash('Item removed from cart', 'info')
    else:
        cart_item.quantity = quantity
        flash('Cart updated', 'success')
    
    db.session.commit()
    return redirect(url_for('view_cart'))

# Remove item from cart
@app.route('/cart/remove/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    
    if cart_item.session_id != session['cart_session_id']:
        flash('Unauthorized', 'error')
        return redirect(url_for('view_cart'))
    
    product_name = cart_item.product.name
    db.session.delete(cart_item)
    db.session.commit()
    
    flash(f'Removed {product_name} from cart', 'success')
    return redirect(url_for('view_cart'))

# Cleanup unavailable items from cart
@app.route('/cart/cleanup', methods=['POST'])
def cleanup_cart():
    cart_items = CartItem.query.filter_by(session_id=session['cart_session_id']).all()
    
    removed_count = 0
    for item in cart_items:
        if not item.product.is_available_for_purchase():
            db.session.delete(item)
            removed_count += 1
    
    db.session.commit()
    
    if removed_count > 0:
        flash(f'✓ Removed {removed_count} unavailable item(s) from your cart', 'warning')
    else:
        flash('All items in your cart are available', 'success')
    
    return redirect(url_for('view_cart'))

# View cart
@app.route('/cart')
def view_cart():
    cart_items = CartItem.query.filter_by(session_id=session['cart_session_id']).all()
    
    # Check for unavailable items
    has_unavailable = any(not item.product.is_available_for_purchase() for item in cart_items)
    
    # Calculate total only for available items
    total = sum(
        item.product.price * item.quantity 
        for item in cart_items 
        if item.product.is_available_for_purchase() and item.product.price
    )
    
    return render_template('cart.html', 
                         cart_items=cart_items, 
                         total=total,
                         has_unavailable=has_unavailable)

# Checkout page
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = CartItem.query.filter_by(session_id=session['cart_session_id']).all()
    
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('index'))
    
    # Check for unavailable items before checkout
    unavailable_items = [item for item in cart_items if not item.product.is_available_for_purchase()]
    
    if unavailable_items:
        for item in unavailable_items:
            flash(f'❌ "{item.product.name}" is no longer available. Please remove it from cart.', 'error')
        return redirect(url_for('view_cart'))
    
    if request.method == 'POST':
        # Process order
        user_email = request.form.get('user_email')
        shipping_address = request.form.get('shipping_address')
        
        if not user_email or not shipping_address:
            flash('Please provide both email and shipping address', 'error')
            total = sum(item.product.price * item.quantity for item in cart_items)
            return render_template('checkout.html', cart_items=cart_items, total=total)
        
        # Calculate total
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        # Create order
        order_id = str(uuid.uuid4())
        order = Order(
            id=order_id,
            user_email=user_email,
            shipping_address=shipping_address,
            total_amount=total,
            status='pending'
        )
        
        # Create order items
        for cart_item in cart_items:
            order_item = OrderItem(
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            order.items.append(order_item)
            db.session.delete(cart_item)  # Clear from cart
        
        db.session.add(order)
        db.session.commit()
        
        flash(f'✅ Order placed successfully! Order ID: {order.id}', 'success')
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    # GET request - show checkout form
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('checkout.html', cart_items=cart_items, total=total)

# Order confirmation
@app.route('/order/<order_id>')
def order_confirmation(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_confirmation.html', order=order)

# Product details
@app.route('/product/<product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

def perform_scraping(url):
    """Improved scraping with better error handling"""
    try:
        # Add headers to avoid being blocked
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        products = []
        
        # Try multiple common product selectors
        product_selectors = [
            '.product', '.product-item', '.product-card', 
            '.item', '.product-listing', '[data-product-id]',
            'article', '.product-container'
        ]
        
        product_elements = []
        for selector in product_selectors:
            product_elements = soup.select(selector)
            if product_elements:
                print(f"Found {len(product_elements)} products using selector: {selector}")
                break
        
        # If still no products, look for price elements as fallback
        if not product_elements:
            price_elements = soup.select('.price, .product-price, .sale-price')
            if price_elements:
                # Create artificial product elements from price elements
                for price_elem in price_elements[:10]:  # Limit to 10
                    product_elements.append(price_elem.parent)
        
        for product_elem in product_elements:
            product = scraper.scrape_product(product_elem)
            if product.name != "Unknown Product":  # Only add valid products
                products.append(product)
        
        if not products:
            # Provide helpful message
            print(f"No products found on {url}. The page might not have standard product markup.")
            
        return products
        
    except requests.RequestException as e:
        raise Exception(f"Failed to fetch URL: {str(e)}")
    except Exception as e:
        raise Exception(f"Scraping error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)