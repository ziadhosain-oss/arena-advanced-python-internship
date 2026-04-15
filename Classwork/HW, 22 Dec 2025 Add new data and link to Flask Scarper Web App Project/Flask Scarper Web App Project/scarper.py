from database import products_collection
import requests
from bs4 import BeautifulSoup
import time

# Clear previous data
products_collection.delete_many({})

# URL to scrape - Using books.toscrape.com (a practice scraping website)
base_url = "https://books.toscrape.com"
url = f"{base_url}/catalogue/page-1.html"

try:
    # Set headers to mimic browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all product articles
    products = soup.find_all("article", class_="product_pod")
    
    if not products:
        print("❌ No products found! Check selectors or URL.")
    else:
        for item in products:
            try:
                # Extract product name
                name = item.find("h3").find("a")["title"]
                
                # Extract product price
                price = item.find("p", class_="price_color").text.strip()
                
                # Extract product link
                link = item.find("h3").find("a")["href"]
                
                # Convert relative to absolute URL
                if link.startswith("/"):
                    link = f"{base_url}/catalogue/{link}"
                elif not link.startswith("http"):
                    link = f"{base_url}/catalogue/{link}"
                
                product = {
                    "name": name,
                    "price": price,
                    "product_url": link
                }
                
                # Insert product into MongoDB
                products_collection.insert_one(product)
                print(f"✓ Inserted: {name} - {price}")
                
            except Exception as e:
                print(f"Error processing item: {str(e)}")
                continue
        
        print(f"\n✓ Scraping complete! {products_collection.count_documents({})} products inserted.")
        
except requests.exceptions.RequestException as e:
    print(f"Error fetching page: {str(e)}")
except Exception as e:
    print(f"Error: {str(e)}")
