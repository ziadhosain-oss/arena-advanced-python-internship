import requests
from bs4 import BeautifulSoup
def scrape_product(query):
    url = f"https://www.startech.com.bd/product/search?search={query}"
    print("Scraping URL:", url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept-Language": "en-US,en;q=0.9",
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    products_soup = soup.find_all('div', class_='p-item')

    products = []
    for product in products_soup:
        # print(product)
        name = product.find('h4', class_='p-item-name').text.strip()
        price = product.find('div', class_='p-item-price')
        if price.find('span', class_='price-new'):
            price = price.find('span', class_='price-new').text.strip()
        else:
            price = price.text.strip()

        product_url = product.find('div', class_='p-item-img').find('a')['href']
        img_url = product.find('img')['src']
        products.append(
            {
                'name': name,
                'price': price,
                'img_url': img_url,
                'product_url': product_url
            }
        )
    return products



if __name__ == "__main__":
    results = scrape_product("laptop")
    print(results)