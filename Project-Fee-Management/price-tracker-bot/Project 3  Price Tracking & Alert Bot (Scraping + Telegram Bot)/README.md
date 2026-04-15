# Price Tracking & Alert Bot

A simple price tracking bot that scrapes product pages from supported Bangladesh e-commerce sites and sends Telegram alerts when prices drop below a target.

## Features

- Web UI using Flask to view all tracked products
- Telegram bot to register product URLs and target prices
- Playwright-based scraper for Daraz, Chaldal, and Startech
- MongoDB storage for tracked products and price history
- Scheduler to periodically check prices and send alerts

## Requirements

- Python 3.8+
- MongoDB running locally at `mongodb://localhost:27017/`
- Telegram bot token

## Installation

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the environment:

```powershell
venv\Scripts\Activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:

```bash
python -m playwright install
```

## Configuration

Edit `bot.py` and `scheduler.py` to set your Telegram bot token:

```python
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
```

Ensure MongoDB is running locally before starting the app.

## Usage

- Start the web interface:

```bash
python app.py
```

- Start the Telegram bot:

```bash
python bot.py
```

- Run the scheduler to check prices automatically every 6 hours:

```bash
python scheduler.py
```

## Supported Sites

- Daraz
- Chaldal
- Startech

## Files

- `app.py` - Flask web app for viewing tracked products
- `bot.py` - Telegram bot for adding tracked products
- `scheduler.py` - Periodic price checker and alert sender
- `scraper.py` - Product scraping logic using Playwright
- `db.py` - MongoDB helper functions
- `templates/index.html` - Web UI template
