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


def open_website(url):
    global browser, current_page

    start_browser()

    # If page was closed, create a new one
    if current_page is None or current_page.is_closed():
        current_page = browser.new_page()

    print("Opening:", url)

    current_page.goto(url)


def search_on_page(query, selector=None):

    global current_page

    if current_page is None or current_page.is_closed():
        print("No active browser page")
        return

    try:

        current_page.wait_for_timeout(2000)

        # Detect website automatically
        if "youtube" in current_page.url:
            selector = 'input[name="search_query"]'

        elif "google" in current_page.url:
            selector = 'input[name="q"]'

        if selector is None:
            print("No selector for this site")
            return

        current_page.wait_for_selector(selector, timeout=15000)

        current_page.fill(selector, query)

        current_page.keyboard.press("Enter")

        print("Searching:", query)

    except Exception as e:

        print("Search failed:", e)