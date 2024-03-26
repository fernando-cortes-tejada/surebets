import time
from playwright.sync_api import Page
from playwright.sync_api import Locator


def get_game_list(page: Page, timeout: int = 10) -> Locator:
    wait_game_list = page.wait_for_selector(
        ".contentBlock.square",
        timeout=timeout * 1000,
    )
    visible_game_list = wait_game_list.is_visible()
    if visible_game_list:
        return page.locator(".contentBlock.square")
    return []


def get_games_url(game_list: Locator) -> list[str]:
    games = game_list.locator(
        "xpath=//a[starts-with(@href, '/es/basketball/nba')]"
    ).all()
    games_url = []
    for game in games:
        game_url = game.get_attribute("href")
        games_url.append(game_url)
    return games_url
