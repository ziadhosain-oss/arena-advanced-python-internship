from database import products_collection
import requests
from bs4 import BeautifulSoup

def scrape_data():
    # Scrape from StarTech BD - popular products or search for common terms
    queries = ["laptop", "monitor", "keyboard", "mouse"]

    for query in queries:
        url = f"https://www.startech.com.bd/product/search?search={query}"
        print(f"Scraping URL: {url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Failed to fetch {url}, status code: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            products = soup.find_all('div', class_='p-item')

            for item in products:
                try:
                    # Extract product name
                    name_elem = item.find("h4", class_="p-item-name")
                    if not name_elem:
                        continue
                    name = name_elem.text.strip()

                    # Extract product price
                    price_elem = item.find("div", class_="p-item-price")
                    if not price_elem:
                        continue
                    price = price_elem.text.strip()

                    # Extract product link
                    link_elem = item.find("a", href=True)
                    if not link_elem:
                        continue
                    link = link_elem["href"]

                    # Make sure link is absolute
                    if link.startswith("/"):
                        link = "https://www.startech.com.bd" + link

                    product = {
                        "name": name,
                        "price": price,
                        "product_url": link
                    }

                    # Avoid duplicates by checking if the link exists
                    if not products_collection.find_one({"product_url": link}):
                        products_collection.insert_one(product)
                        print(f"Added product: {name}")

                except Exception as e:
                    print(f"Error processing product: {e}")
                    continue

        except Exception as e:
            print(f"Error scraping {url}: {e}")
            continue

    print("Scraping and insertion complete!")