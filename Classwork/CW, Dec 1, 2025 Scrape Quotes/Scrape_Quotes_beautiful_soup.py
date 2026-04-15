import requests
from bs4 import BeautifulSoup

# Connect + Soup
page = requests.get("http://quotes.toscrape.com")
soup = BeautifulSoup(page.text, "html.parser")

# Locate + Extract
for q in soup.find_all("div", class_="quote"):
    text = q.find("span", class_="text").get_text()
    author = q.find("small", class_="author").get_text()
    tags = [t.get_text() for t in q.find("div", class_="tags").find_all("a", class_="tag")]
    
    # Output
    print(f"Quote: {text}")
    print(f"Author: {author}")
    print(f"Tags: {', '.join(tags)}")
    print("-" * 60)