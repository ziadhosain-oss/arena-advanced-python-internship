# Scraper Telegram Bot

This is a Telegram bot that scrapes product information from Startech website.

## Features

- Search for products using /search command
- Returns top 5 products with name, photo, link, and price
- Web API for scraping

## Installation

1. Install dependencies: pip install -r requirements.txt

## Usage

2. Run the bot and web API: python run.py

Send /search Mac Mini m4 to the bot to search for products.

Web API: GET /search/<query> returns JSON with products.