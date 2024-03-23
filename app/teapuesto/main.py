from app.utils import initiate_browser, close_session
from app.teapuesto.entities import NBA_URL
from app.teapuesto import utils

from playwright.sync_api import Page, Browser, Playwright
from playwright.sync_api import Locator


def scrape() -> list[dict]:
    info = []

    page, browser, playwright = initiate_browser(headless=False)
    page.goto(NBA_URL)

    games = utils.get_game_list(page)

    if games is None:
        close_session(browser, playwright)
        return info

    for i, game in enumerate(games):
        info = handle_game(page, game, info)

        print(f"{i} of {len(games)-1}")

        if i == len(games) - 1:
            print("break")
            break

        print("clicking back")
        page.goto(NBA_URL)
        game_list_visible = utils.wait_game_list_visible(page)
        if not game_list_visible:
            break

    print("Done!")

    close_session(browser, playwright)
    return info


def handle_game(page: Page, game: Locator, info: list[dict]) -> list[dict]:
    game.click()

    if not utils.check_game_page(page):
        return info

    game_name = page.locator(".team-name").text_content()
    carousels = utils.get_carousels(page)

    print(game_name)

    for carousel in carousels:
        if "Apuestas Generales" not in carousel.text_content():
            carousel.click()

        markets = utils.get_markets(page)

        if not markets:
            continue

        for market in markets:
            info.extend(utils.get_info(market, game_name))

    return info


info = scrape()
