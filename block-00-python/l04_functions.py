from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import expect

BASE_URL = "https://www.saucedemo.com/"
USERS = ["standard_user", "problem_user", "performance_glitch_user", "error_user", "visual_user"]
PASSWORD = "secret_sauce"


def login(page: Page, username: str, password: str = PASSWORD) -> None:
    """Відкриває сайт і логіниться."""
    page.goto(BASE_URL)
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Login").click()
    expect_page = "https://www.saucedemo.com/inventory.html"
    expect(page, f"Очікували сторінку {expect_page}").to_have_url(expect_page)


def parse_price(text: str) -> float:
    """'$29.99' -> 29.99"""
    return float(text.replace("$", ""))


def get_prices(page: Page) -> list[float]:
    """Збирає всі ціни на сторінці як float."""
    price_text = page.locator(".inventory_item_price").all_inner_texts()
    return [float(price.replace("$", "")) for price in price_text]


def sort_by(page: Page, label: str) -> None:
    """Вибирає сортування за видимим текстом, напр. 'Price (low to high)'."""
    page.locator("[data-test='product-sort-container']").select_option(label=label)


def is_sorted(values: list, reverse: bool = False) -> bool:
    """True, якщо список уже відсортований."""
    return values == sorted(values, reverse=reverse)



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    login(page, "standard_user")
    sort_by(page, "Price (low to high)")
    prices = get_prices(page)
    assert is_sorted(get_prices(page)), f"Сортування зламане: {prices}"
    print(f"✅ low→high: {prices}")

    sort_by(page, "Price (high to low)")
    prices2 = get_prices(page)
    assert is_sorted(prices2, reverse=True), f"Сортування зламане: {prices2}"
    print(f"✅ high→low: {prices2}")

    # Перевірка всіх юзерів
    print("\n----------ALL Users------------")
    for user in USERS:
        print(f"\nТест для юзера = {user}")
        login(page, user)
        sort_by(page, "Price (low to high)")
        prices = get_prices(page)
        if is_sorted(prices):
            print(f"✅ low→high: {prices}. User = {user}: ✅")
        else:
            print(f"Сортування зламане: {prices}. User = {user}: ❌")

        sort_by(page, "Price (high to low)")
        prices2 = get_prices(page)
        if is_sorted(prices2, reverse=True):
            print(f"✅ high→low: {prices2}. User = {user}: ✅")
        else:
            print(f"Сортування зламане: {prices2}. User = {user}: ❌")

    browser.close()