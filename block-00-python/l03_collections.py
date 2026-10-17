from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standard_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.get_by_role("button", name="Login").click()

    names = page.locator(".inventory_item_name").all_inner_texts()
    prices_text = page.locator(".inventory_item_price").all_inner_texts()

    # --- А. Список ---
    print(len(names))
    print(f"{names[0]}, {names[-1]}")

    # --- Б. Цикл ---
    prices = []
    for price in prices_text:
        prices.append(float(price.replace("$", "")))

    prices2 = [float(price.replace("$", "")) for price in prices_text]
    print(prices == prices2)

    # --- В. Агрегати ---
    print(f"Total: ${sum(prices):.2f}")
    print(f"Max price:${max(prices):.2f}, Min price:${min(prices):.2f}")

    # --- Г. Словник ---
    products = {}
    for name, price in zip(names, prices):
        products[name] = price
    print(products)
    print(products["Sauce Labs Onesie"])
    for name, price in products.items():
        if price > 15:
            print(f"{name}: ${price:.2f}")

    # --- Д. Перевірка (assert = справжній тест) ---
    assert all(p > 0 for p in list(products.values())), f"Товари мають бути більше 0, а маємо {products.values()}"
    print(f"Товари більше 0")
    # assert <умова>, "повідомлення, якщо впало"
    browser.close()