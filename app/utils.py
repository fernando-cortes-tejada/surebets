from playwright.sync_api import sync_playwright
from playwright.sync_api import Page, Browser, Playwright


def initiate_browser(headless: bool = True) -> tuple[Page, Browser, Playwright]:
    """Initiate the browser in chromium, with the option to run headless or not.

    Args:
        headless (bool, optional): Boolean to decide if to run headless. Defaults to True.

    Returns:
        tuple[Page, Browser, Playwright]: The page, browser and playwright objects.
    """
    playwright = sync_playwright().start()

    browser = playwright.chromium.launch(
        headless=headless,
        args=["--window-size=1920,1080"],
    )
    page = browser.new_page()

    return page, browser, playwright


def close_session(browser: Browser, playwright: Playwright):
    """Close the browser and stop the playwright.

    Args:
        browser (Browser): The browser object.
        playwright (Playwright): The playwright object.
    """
    browser.close()
    playwright.stop()
