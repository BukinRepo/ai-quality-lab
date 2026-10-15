from playwright.sync_api import sync_playwright

USERNAME = "standard_user"      # КАПСОМ = константа (домовленість, не правило мови)
PASSWORD = "secret_sauce"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")

    page.get_by_placeholder("Username").fill(USERNAME)
    page.get_by_placeholder("Password").fill(PASSWORD)
    page.get_by_role("button", name="Login").click()

    # --- Завдання А: URL ---
    current_url = page.url
    print(f"{current_url=}")
    print(current_url.split("/")[-1])
    print(current_url.endswith(".html"))

    # --- Завдання Б: ціна першого товару ---
    price_text = page.locator(".inventory_item_price").first.inner_text()
    print(f"{price_text=}, тип: {type(price_text)}")
    price = float(price_text.strip("$"))
    print(type(price))
    # --- Завдання В: розрахунок ---
    qty = 3
    total = price * qty
    total_text = f"${total:.2f}"
    print(f"{qty} x {price_text} = {total_text}")

    # --- Завдання Г: назва товару ---
    name = page.locator(".inventory_item_name").first.inner_text()
    print(name.upper())
    print("Backpack" in name)


    page.locator(".inventory_item_name").first.click()
    inner_price = float(page.locator(".inventory_details_price").first.inner_text().strip("$"))
    print(inner_price == price)

    browser.close()