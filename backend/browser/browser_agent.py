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

    current_page = browser.new_page()

    print("Opening:", url)

    current_page.goto(url)


def search_on_page(query, selector):

    global current_page

    if current_page is None:
        print("No active browser page")
        return

    try:

        # wait for the input field to appear
        current_page.wait_for_selector(selector, timeout=15000)

        # type the query
        current_page.fill(selector, query)

        # press enter
        current_page.keyboard.press("Enter")

        print("Searching:", query)

    except Exception as e:

        print("Search failed:", e)