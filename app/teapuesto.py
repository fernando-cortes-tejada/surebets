from playwright.sync_api import sync_playwright

playwright = sync_playwright().start()

# start maximized and no viewport size
browser = playwright.chromium.launch(headless=False, args=["--window-size=1920,1080"])
page = browser.new_page()
page.goto(
    "https://www.teapuesto.pe/sport/odds?timeFrame=all&tournaments=193912&type=matches"
)

game_list = page.locator(".market-table.ng-star-inserted")
days = game_list.locator(".group-events-table")
games = days.locator(".overflow-ellipsis")

games = games.all()
games = games[1::2]

games[0].click()


browser.close()

playwright.stop()
