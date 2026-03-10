# browser/browser_agent.py

from playwright.sync_api import sync_playwright

playwright_instance = None
browser = None
current_page = None


def start_browser():
    global playwright_instance, browser

    if playwright_instance is None:
        playwright_instance = sync_playwright().start()
        browser = playwright_instance.chromium.launch(headless=False)


def ensure_page():
    """Ensure we always have a valid browser page"""
    global browser, current_page

    if browser is None:
        start_browser()

    try:
        if current_page is None or current_page.is_closed():
            current_page = browser.new_page()
    except:
        current_page = browser.new_page()


def open_website(url):
    global current_page

    start_browser()
    ensure_page()

    try:
        print("Opening:", url)
        current_page.goto(url)

    except:
        # If page crashed, recreate it
        print("Page crashed, recreating tab...")

        current_page = browser.new_page()
        current_page.goto(url)


def search_on_page(query, selector=None):

    global current_page

    ensure_page()

    try:

        current_page.wait_for_timeout(2000)

        # Auto detect website
        if "youtube" in current_page.url:
            selector = 'input[name="search_query"]'

        elif "google" in current_page.url:
            selector = 'input[name="q"]'

        if selector is None:
            print("No selector available")
            return

        current_page.wait_for_selector(selector, timeout=15000)

        current_page.fill(selector, query)

        current_page.keyboard.press("Enter")

        print("Searching:", query)

    except Exception as e:

        print("Search failed:", e)