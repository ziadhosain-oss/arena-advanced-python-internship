# Flask Scraper Web App Project

A modern Flask web application that scrapes product data from websites and displays them in a sleek dashboard.

## Features

✓ **Web Scraping** - Automatically scrapes product names, prices, and links  
✓ **MongoDB Integration** - Stores scraped data in MongoDB  
✓ **Responsive UI** - Beautiful Bootstrap-based dashboard  
✓ **Direct Links** - Click "View Details Source" to open products in a new tab  
✓ **Error Handling** - Robust error handling and logging  

## Project Structure

```
Flask Scraper Web App Project/
├── app.py              # Flask application and routes
├── scarper.py          # Web scraping script
├── templates/
│   └── index.html      # Dashboard template (Bootstrap)
└── README.md           # This file
```

## Requirements

- Python 3.7+
- MongoDB (running locally on port 27017)
- Required Python packages:
  - Flask
  - pymongo
  - requests
  - beautifulsoup4

## Installation

1. **Install Python packages:**
   ```bash
   pip install flask pymongo requests beautifulsoup4
   ```

2. **Start MongoDB:**
   - On Windows: `mongod`
   - On Mac/Linux: `mongod`

3. **Run the scraper to fetch data:**
   ```bash
   python scarper.py
   ```

4. **Start the Flask app:**
   ```bash
   python app.py
   ```

5. **Open your browser:**
   - Navigate to `http://localhost:5000`

## Usage

1. **Scrape Data:**
   - Run `python scarper.py` to fetch products from books.toscrape.com
   - The scraper stores name, price, and product URL in MongoDB

2. **View Products:**
   - Open `http://localhost:5000` to see the dashboard
   - Products are displayed in a grid layout

3. **Access Product Links:**
   - Click "View Details Source" button on any product card
   - Opens the original product page in a new tab

## Customization

To scrape from a different website:

1. Update the `url` in `scarper.py`
2. Modify the CSS selectors to match the target website structure:
   ```python
   name = item.find("h3").find("a")["title"]  # Update selector
   price = item.find("p", class_="price_color").text.strip()  # Update selector
   link = item.find("h3").find("a")["href"]  # Update selector
   ```

## Current Source

- **Website:** https://books.toscrape.com
- **Data:** Book listings with prices and links
- **Update:** Run `scarper.py` anytime to refresh the database

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No Data Found!" | Run `python scarper.py` first to fetch data |
| MongoDB connection error | Ensure MongoDB is running (`mongod` in terminal) |
| Products not displaying | Check browser console for errors (F12) |
| 404 errors on product links | The source website may have changed structure |

## Technologies Used

- **Backend:** Flask (Python web framework)
- **Database:** MongoDB (NoSQL database)
- **Frontend:** Bootstrap 5, HTML, CSS
- **Scraping:** BeautifulSoup 4, Requests
- **Styling:** Custom CSS with Bootstrap

## License

© 2025 Flask Scraper Project - Educational Purpose
