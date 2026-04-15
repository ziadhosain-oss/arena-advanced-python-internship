# scraper.py
import re
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum

class ProductStatus(Enum):
    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    UPCOMING = "upcoming"

@dataclass
class Product:
    id: str
    name: str
    price: Optional[float]
    status: ProductStatus
    original_price_text: str
    url: str
    
class WebScraper:
    def __init__(self):
        self.price_patterns = [
            r'\$\s*(\d+(?:,\d{3})*(?:\.\d{2})?)',  # $49.99
            r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*USD',  # 49.99 USD
            r'(\d+(?:\.\d{2})?)'  # plain number
        ]
    
    def extract_price(self, price_text: str) -> Optional[float]:
        """Extract numeric price from text, return None if not a valid price"""
        if not price_text:
            return None
            
        # Clean the text
        price_text = price_text.strip().lower()
        
        # Check for non-price indicators
        if any(keyword in price_text for keyword in ['out of stock', 'out-of-stock', 'outofstock']):
            return None
            
        if any(keyword in price_text for keyword in ['up coming', 'upcoming', 'coming soon']):
            return None
            
        # Try to extract numeric price
        for pattern in self.price_patterns:
            match = re.search(pattern, price_text)
            if match:
                price_str = match.group(1).replace(',', '')
                try:
                    return float(price_str)
                except ValueError:
                    continue
        return None
    
    def determine_product_status(self, price_element_text: str) -> ProductStatus:
        """Determine product status based on price element text"""
        text_lower = price_element_text.strip().lower()
        
        if any(keyword in text_lower for keyword in ['out of stock', 'out-of-stock', 'outofstock']):
            return ProductStatus.OUT_OF_STOCK
            
        if any(keyword in text_lower for keyword in ['up coming', 'upcoming', 'coming soon']):
            return ProductStatus.UPCOMING
            
        # If we have a valid price, it's in stock
        price = self.extract_price(price_element_text)
        if price is not None:
            return ProductStatus.IN_STOCK
            
        # Default to out of stock if uncertain
        return ProductStatus.OUT_OF_STOCK
    
    def scrape_product(self, product_element) -> Product:
        """Scrape a single product with proper status handling"""
        # This is a simplified example - you'll need to adapt selectors
        # based on the website you're scraping
        
        # Example: try to find name and price elements
        try:
            # Try common selectors - adjust based on your HTML
            name_elem = product_element.find(['.product-name', '.product-title', 'h3', '.name'])
            price_elem = product_element.find(['.price', '.product-price', '.sale-price', '.current-price'])
            
            product_name = name_elem.text.strip() if name_elem else "Unknown Product"
            price_text = price_elem.text.strip() if price_elem else ""
            
            # Determine status
            status = self.determine_product_status(price_text)
            price = self.extract_price(price_text) if status == ProductStatus.IN_STOCK else None
            
            # Try to get product URL
            link_elem = product_element.find('a')
            product_url = link_elem.get('href', '') if link_elem else ''
            
            return Product(
                id=self.generate_product_id(product_name),
                name=product_name,
                price=price,
                status=status,
                original_price_text=price_text,
                url=product_url
            )
        except Exception as e:
            # Return a default product if scraping fails
            return Product(
                id=self.generate_product_id("unknown"),
                name="Unknown Product",
                price=None,
                status=ProductStatus.OUT_OF_STOCK,
                original_price_text="Error scraping",
                url=""
            )
    
    def generate_product_id(self, product_name: str) -> str:
        """Generate a unique product ID"""
        import hashlib
        return hashlib.md5(product_name.encode()).hexdigest()[:12]