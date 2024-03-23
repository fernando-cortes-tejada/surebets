from playwright.sync_api import sync_playwright

playwright = sync_playwright().start()

# start maximized and no viewport size
browser = playwright.chromium.launch(headless=False, args=["--window-size=1920,1080"])
page = browser.new_page()
# page.goto("https://www.pinnacle.com/es/basketball/nba/matchups")
page.goto(
    "https://www.teapuesto.pe/sport/odds?timeFrame=all&tournaments=193912&type=matches"
)

game_list = page.locator(".contentBlock.square")
games = game_list.locator(".style_row__yBzX8.style_row__12oAB")
links = games.get_by_role("link").all()

links = [link.get_attribute("href") for link in links]


browser.close()

playwright.stop()
