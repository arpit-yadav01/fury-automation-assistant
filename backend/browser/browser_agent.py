# browser/browser_agent.py

from playwright.sync_api import sync_playwright

playwright_instance = None
browser = None


def open_website(url):
    global playwright_instance, browser

    if playwright_instance is None:
        playwright_instance = sync_playwright().start()
        browser = playwright_instance.chromium.launch(headless=False)

    page = browser.new_page()

    print("Opening:", url)

    page.goto(url)