from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    page.locator("[data-test='product-sort-container']").select_option(label="Price (low to high)")

    # Сортування та перевірка
    prices_text = page.locator(".inventory_item_price").all_inner_texts()
    prices = [float(price.replace("$", "")) for price in prices_text]
    assert prices == sorted(prices), f"Сортування ціни зламане: {prices}"
    print("✅ Сортування за ціною працює")

    page.locator("[data-test='product-sort-container']").select_option(label="Name (Z to A)")
    names = page.locator(".inventory_item_name").all_inner_texts()
    assert names == sorted(names, reverse= True), f"Сортування за назвою зламане: {names}"
    print("✅ Сортування за назвою працює")
    browser.close()