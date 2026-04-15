# models.py
from datetime import datetime
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

# Create db instance here
db = SQLAlchemy()

class ProductStatus(Enum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    UPCOMING = "upcoming"

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=True)
    status = db.Column(db.Enum(ProductStatus), nullable=False, default=ProductStatus.OUT_OF_STOCK)
    original_price_text = db.Column(db.String(100))
    url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def is_available_for_purchase(self) -> bool:
        """Check if product can be purchased"""
        return self.status == ProductStatus.IN_STOCK and self.price is not None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'status': self.status.value,
            'is_available': self.is_available_for_purchase(),
            'original_price_text': self.original_price_text,
            'url': self.url
        }

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String(50), db.ForeignKey('products.id'), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref='cart_items')
    
    def validate(self):
        """Validate cart item before operations"""
        if not self.product.is_available_for_purchase():
            raise ValueError(f"Product '{self.product.name}' is not available for purchase (Status: {self.product.status.value})")

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.String(50), primary_key=True)
    user_email = db.Column(db.String(120), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(50), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(50), db.ForeignKey('products.id'), nullable=False)
    product_name = db.Column(db.String(200))
    price_at_purchase = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    
    def __init__(self, product, quantity):
        self.product_id = product.id
        self.product_name = product.name
        self.price_at_purchase = product.price
        self.quantity = quantity