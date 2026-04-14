import asyncio
from playwright.async_api import async_playwright

async def scrape_product(url: str) -> dict:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            await page.goto(url, timeout=60000)
            
            # Wait for content to load
            await page.wait_for_load_state('networkidle')
            
            # Determine site and selectors
            if 'daraz' in url.lower():
                title_selector = 'h1.pdp-product-title'
                price_selector = '.pdp-price'
            elif 'chaldal' in url.lower():
                title_selector = 'h1.product-title'
                price_selector = '.price'
            elif 'startech' in url.lower():
                title_selector = 'h1.product-title'
                price_selector = '.price'
            else:
                raise ValueError("Unsupported site. Only Daraz, Chaldal, and Startech are supported.")
            
            # Extract title
            title_element = await page.query_selector(title_selector)
            if title_element:
                title = await title_element.inner_text()
                title = title.strip()
            else:
                title = "Title not found"
            
            # Extract price
            price_element = await page.query_selector(price_selector)
            if price_element:
                price = await price_element.inner_text()
                price = price.strip()
            else:
                price = "Price not found"
            
            return {"title": title, "price": price}
        
        finally:
            await browser.close()

async def test(url: str):
    async with async_playwright() as p:
        # Launch browser with UI so you can see the page
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        # Go to the product URL
        await page.goto(url, timeout=60000)

        # Print the entire HTML content to the console
        html = await page.content()
        print(html)

        # Close browser
        await browser.close()

if __name__ == "__main__":
    # Replace with a real product link from StarTech, Daraz, or Chaldal
    asyncio.run(test("https://www.startech.com.bd/hp-15-fc0355au-laptop"))