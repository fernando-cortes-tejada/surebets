import time
from playwright.sync_api import Page
from playwright.sync_api import Locator


def get_game_list(page: Page, timeout: int = 10) -> list[Locator]:
    visible_game_list = wait_game_list_visible(page, timeout=timeout)

    if visible_game_list:
        game_list = page.locator(".market-table.ng-star-inserted")
        days = game_list.locator(".group-events-table")
        games = days.locator(".overflow-ellipsis")
        games = games.all()

        no_duplicate_games = []
        for i in range(1, len(games), 2):
            no_duplicate_games.append(games[i])
        return no_duplicate_games

    else:
        return []


def wait_game_list_visible(page: Page, timeout: int = 10) -> bool:
    t1 = time.time()
    t2 = time.time()

    visible_game_list = False

    while (not visible_game_list) and ((t2 - t1) < timeout):
        game_list = page.wait_for_selector(
            ".market-table.ng-star-inserted",
            timeout=timeout * 1000,
        )
        visible_game_list = game_list.is_visible()
        t2 = time.time()

    return visible_game_list


def check_game_page(page: Page, timeout: int = 10) -> bool:
    # Initiate the timer
    t1 = time.time()
    t2 = time.time()

    visible_game_page = False

    while (not visible_game_page) and ((t2 - t1) < timeout):
        game_page = page.wait_for_selector(
            ".nav.nav-tabs",
            timeout=timeout * 1000,
        )
        visible_game_page = game_page.is_visible()
        t2 = time.time()

    return visible_game_page


def get_carousels(page: Page) -> list[Locator]:
    carousels = page.locator(".nav.nav-tabs").locator(".nav-item.ng-star-inserted")
    carousels = carousels.all()

    return carousels


def get_markets(page: Page) -> list[str]:
    markets_table = page.locator(".extra-odds-accordion-container")
    markets = markets_table.all_inner_texts()

    markets = list(filter(lambda market: "\n" in market, markets))

    return markets


def get_info(string: str, game_name: str, teams: list[str]) -> list[dict]:
    info = []

    string_list = string.split("\n")

    market = string_list[0]
    market = market.split("(")[0].strip()

    match market:
        case "Ganador":
            info.extend(info_winner(game_name, teams, string_list))
        case "Total":
            info.append(info_total(game_name, string_list))
        case "Hándicap":
            info.append(info_handicap(game_name, teams, string_list))
        case "1 total" | "home total" | "Local total":
            info.append(info_total_team(game_name, teams[0], string_list))
        case "2 total" | "away total" | "Visitante total":
            info.append(info_total_team(game_name, teams[1], string_list))
        case "1º Mitad - hándicap":
            info.append(
                info_handicap(game_name, teams, string_list, "handicap_first_half")
            )
        case "1st half - total":
            info.append(info_total(game_name, string_list, "total_first_half"))
        case "1er cuarto - hándicap":
            info.append(
                info_handicap(game_name, teams, string_list, "handicap_first_quarter")
            )
        case "2do cuarto - hándicap":
            info.append(
                info_handicap(game_name, teams, string_list, "handicap_second_quarter")
            )

    return info


def info_winner(game_name: str, teams: list[str], string_list: list[str]) -> list[dict]:
    info = []
    string_list = string_list[1:]
    for i in range(2):
        data_ = string_list[(i * 2) + 1]
        info.append(
            {
                "website": "teapuesto",
                "game": game_name,
                "market": "winner",
                "team": teams[i],
                "more": float(data_),
            }
        )

    return info


def info_total(game_name: str, string_list: list[str], market: str = "total") -> dict:
    string_list = string_list[-4:]

    info = {
        "website": "teapuesto",
        "game": game_name,
        "market": market,
        "line": float(string_list[0].split(" ")[-1]),
        "more": float(string_list[1]),
        "less": float(string_list[3]),
    }

    return info


def info_handicap(
    game_name: str, teams: list[str], string_list: list[str], market: str = "handicap"
) -> dict:
    string_list = string_list[1:]

    info = {
        "website": "teapuesto",
        "game": game_name,
        "market": market,
        "team": teams[0],
        "line": float(string_list[0].split(" ")[-1].replace("(", "").replace(")", "")),
        "more": float(string_list[1]),
        "less": float(string_list[3]),
    }

    return info


def info_total_team(game_name: str, team: str, string_list: list[str]) -> dict:
    string_list = string_list[1:]

    info = {
        "website": "teapuesto",
        "game": game_name,
        "market": "total_team",
        "team": team,
        "line": float(string_list[0].split(" ")[-1]),
        "more": float(string_list[1]),
        "less": float(string_list[3]),
    }

    return info
