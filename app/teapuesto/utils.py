from datetime import datetime
from playwright.sync_api import Page
from playwright.sync_api import Locator


def get_game_list(page: Page, timeout: int = 10) -> list[Locator] | None:
    visible_game_list = wait_game_list_visible(page, timeout=timeout)

    if visible_game_list:
        game_list = page.locator(".market-table.ng-star-inserted")
        days = game_list.locator(".group-events-table")
        games = days.locator(".overflow-ellipsis")
        games = games.all()
        games = games[1::2]
        return games
    else:
        return None


def wait_game_list_visible(page: Page, timeout: int = 10) -> bool:
    t1 = datetime.now()
    t2 = datetime.now()
    visible_game_list = False

    while (not visible_game_list) and ((t2 - t1).seconds < timeout):
        game_list = page.wait_for_selector(
            ".market-table.ng-star-inserted",
            timeout=timeout * 1000,
        )
        visible_game_list = game_list.is_visible()
        t2 = datetime.now()

    return visible_game_list


def check_game_page(page: Page, timeout: int = 10) -> bool:
    # Initiate the timer
    t1 = datetime.now()
    t2 = datetime.now()
    visible_game_page = False

    while (not visible_game_page) and ((t2 - t1).seconds < timeout):
        game_page = page.wait_for_selector(
            ".nav.nav-tabs",
            timeout=timeout * 1000,
        )
        visible_game_page = game_page.is_visible()
        t2 = datetime.now()

    return visible_game_page


def get_carousels(page: Page) -> list[Locator]:
    carousels = page.locator(".nav.nav-tabs")
    carousels = carousels.locator(".nav-item.ng-star-inserted")
    carousels = carousels.all()

    return carousels


def get_markets(page: Page) -> list[str]:
    markets_table = page.locator(".extra-odds-accordion-container")
    markets = markets_table.all_inner_texts()

    markets = [market for market in markets if "\n" in market]

    return markets


def get_info(string: str, game_name: str) -> list[dict]:
    info = []

    string = string.split("\n")

    market = string[0]
    market = market.split("(")[0].strip()

    match market:
        case "Ganador":
            info.extend(info_winner(game_name, string))
        case "Total":
            info.append(info_total(game_name, string))
        case "Hándicap":
            info.append(info_handicap(game_name, string))
        case "1 total" | "home total" | "Local total":
            info.append(info_total_team(game_name, string))
        case "2 total" | "away total" | "Visitante total":
            info.append(info_total_team(game_name, string))
        case "1º Mitad - hándicap":
            info.append(info_handicap(game_name, string, "handicap_first_half"))
        case "1st half - total":
            info.append(info_total(game_name, string, "total_first_half"))
        case "1er cuarto - hándicap":
            info.append(info_handicap(game_name, string, "handicap_first_quarter"))
        case "2do cuarto - hándicap":
            info.append(info_handicap(game_name, string, "handicap_second_quarter"))

    return info


def info_winner(game_name: str, string: str) -> list[dict]:
    info = []
    string = string[1:]
    for i in range(2):
        data_ = string[(i * 2) + 1]
        info.append(
            {
                "website": "teapuesto",
                "game": game_name,
                "market": "winner",
                "more": float(data_),
            }
        )

    return info


def info_total(game_name: str, string: str, market: str = "total") -> dict:
    string = string[-4:]

    info = {
        "website": "teapuesto",
        "game": game_name,
        "market": market,
        "line": float(string[0].split(" ")[-1]),
        "more": float(string[1]),
        "less": float(string[3]),
    }

    return info


def info_handicap(game_name: str, string: list, market: str = "handical") -> dict:
    string = string[1:]

    info = {
        "website": "teapuesto",
        "game": game_name,
        "market": market,
        "line": float(string[0].split(" ")[-1].replace("(", "").replace(")", "")),
        "more": float(string[1]),
        "less": float(string[3]),
    }

    return info


def info_total_team(game_name: str, string: list) -> dict:
    string = string[1:]

    info = {
        "website": "teapuesto",
        "game": game_name,
        "market": "total_team",
        "line": float(string[0].split(" ")[-1]),
        "more": float(string[1]),
        "less": float(string[3]),
    }

    return info
