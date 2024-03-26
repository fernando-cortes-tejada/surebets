from app.utils import initiate_browser, close_session
from app.pinnacle.entities import NBA_URL
from app.pinnacle import utils

from playwright.sync_api import Page
from playwright.sync_api import Locator


def scrape() -> list[dict]:
    try:
        info = []

        page, browser, playwright = initiate_browser(headless=False)
        page.goto(NBA_URL, timeout=60000, wait_until="commit")

        game_list = utils.get_game_list(page)
        games = utils.get_games_url(game_list)

        close_session(browser, playwright)

        if not games:
            close_session(browser, playwright)
            return info

        for game in games[:-1]:
            info.extend(handle_game(page, game))

            page.reload()
            game_list_visible = utils.wait_game_list_visible(page)
            if not game_list_visible:
                break

        # handle the last game without reloading the page
        info.extend(handle_game(page, games[-1]))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        close_session(browser, playwright)

    return info


def handle_game(page: Page, game: Locator) -> list[dict]:
    game.click()

    info = []

    # if the page is not loaded, return the info that we have
    if not utils.check_game_page(page):
        return info

    game_name = page.locator(".team-name").text_content().strip().lower()
    teams = game_name.split(" vs ")
    carousels = utils.get_carousels(page)

    for carousel in carousels:
        if "Apuestas Generales" not in carousel.text_content():
            carousel.click()

        markets = utils.get_markets(page)

        if not markets:
            continue

        for market in markets:
            info.extend(utils.get_info(market, game_name, teams))

    return info
