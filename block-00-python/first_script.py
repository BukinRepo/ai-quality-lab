from playwright.sync_api import sync_playwright   # імпорт: беремо інструмент з бібліотеки

with sync_playwright() as p:                       # with = відкрити і гарантовано закрити ресурс
    browser = p.chromium.launch(headless=False, slow_mo=500)  # видно браузер, кожна дія з паузою 0.5с
    page = browser.new_page()                      # змінна page = нова вкладка

    page.goto("https://playwright.dev/python/")
    title = page.title()                           # метод повертає рядок → кладемо в змінну
    print(f"Заголовок: {title}")                   # f-string: {змінна} підставляється в текст

    page.get_by_role("link", name="Get started").click()
    print(f"Тепер ми на: {page.url}")

    browser.close()