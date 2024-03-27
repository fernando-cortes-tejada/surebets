import time
from playwright.sync_api import Page
from playwright.sync_api import Locator

from app.pinnacle.entities import PINNACLE_URL


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
    future_games = get_future_games(game_list)
    live_games = get_live_games(game_list)

    if live_games:
        games = [game for game in future_games if game not in live_games]
        return games
    return future_games


def get_future_games(game_list: Locator) -> list[str]:
    games = game_list.locator(
        "xpath=//a[starts-with(@href, '/es/basketball/nba')]"
    ).all()
    games_url = []
    for game in games:
        game_url = game.get_attribute("href")
        games_url.append(game_url)
    return list(set(games_url))


def get_live_games(game_list: Locator) -> list[str]:
    games = game_list.locator("xpath=//div[@data-test-id='LiveContainer']")
    games = games.locator(".style_metadata__3MrIC").all()
    games_url = []
    for game in games:
        game_url = game.get_attribute("href")
        games_url.append(game_url)
    return list(set(games_url))
