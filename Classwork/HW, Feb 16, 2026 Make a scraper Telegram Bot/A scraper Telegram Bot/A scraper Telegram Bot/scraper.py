import requests
from bs4 import BeautifulSoup

def scrape_startech(query):
    url = f"https://www.startech.com.bd/index.php?route=product/search&search={query.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    # Find product containers - assuming class 'product-thumb'
    product_divs = soup.find_all('div', class_='product-thumb')
    for div in product_divs[:5]:
        name_elem = div.find('h4', class_='product-name')
        name = name_elem.text.strip() if name_elem else 'No name'
        link_elem = div.find('a')
        link = link_elem['href'] if link_elem and 'href' in link_elem.attrs else ''
        price_elem = div.find('span', class_='price-new')
        price = price_elem.text.strip() if price_elem else 'No price'
        img_elem = div.find('img')
        img = img_elem['src'] if img_elem and 'src' in img_elem.attrs else ''
        products.append({
            'name': name,
            'link': link,
            'price': price,
            'img': img
        })
    return products