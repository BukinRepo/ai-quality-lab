from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import expect

BASE_URL = "https://www.saucedemo.com/"
USERS = ["standard_user", "problem_user", "performance_glitch_user", "error_user", "visual_user"]
PASSWORD = "secret_sauce"
SORT_CASES = [
    {"label": "Price (low to high)", "reverse": False},
    {"label": "Price (high to low)", "reverse": True},
]


def login(page: Page, username: str, password: str = PASSWORD) -> None:
    """Відкриває сайт і логіниться."""
    fill_login_form(page, username, password)
    expect_page = f"{BASE_URL}inventory.html"
    expect(page, f"Очікували сторінку {expect_page}").to_have_url(expect_page)

def fill_login_form(page: Page, username: str, password: str) -> None:
    page.goto(BASE_URL)
    page.get_by_placeholder("Username").fill(username)
    page.get_by_placeholder("Password").fill(password)
    page.get_by_role("button", name="Login").click()

def parse_price(text: str) -> float:
    """'$29.99' -> 29.99"""
    return float(text.replace("$", ""))


def get_prices(page: Page) -> list[float]:
    """Збирає всі ціни на сторінці як float."""
    price_text = page.locator(".inventory_item_price").all_inner_texts()
    return [parse_price(price) for price in price_text]


def sort_by(page: Page, label: str) -> None:
    """Вибирає сортування за видимим текстом, напр. 'Price (low to high)'."""
    page.locator("[data-test='product-sort-container']").select_option(label=label)


def is_sorted(values: list, reverse: bool = False) -> bool:
    """True, якщо список уже відсортований."""
    return values == sorted(values, reverse=reverse)

def check_locked_out_user(browser) -> None:
    context = browser.new_context()
    page = context.new_page()
    page.goto(BASE_URL)
    fill_login_form(page, "locked_out_user", PASSWORD)
    expect(page).to_have_url(BASE_URL)
    expect(page.locator("[data-test='error']")).to_contain_text("locked out")
    print("locked_out_user - work as expected")
    context.close()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    # Перевірка всіх юзерів
    print("\n----------ALL Users------------")
    failures = []
    for user in USERS:
        print(f"\nТест для юзера = {user}")
        context = browser.new_context()
        page = context.new_page()
        try:
            login(page, user)
        except AssertionError as e:
            failures.append(f" User = {user}: логін не вдався — {e}")
            context.close()
            continue
        for case in SORT_CASES:
            sort_by(page, case["label"])
            prices = get_prices(page)
            if is_sorted(prices, case["reverse"]):
                print(f"✅Сортування працює {case['label']}: {prices}. User = {user}: ✅")
            else:
                failures.append(f" User = {user} | {case['label']}: {prices}.")
                print(f"Сортування зламане {case['label']}: {prices}. User = {user}: ❌")
        context.close()
    check_locked_out_user(browser)
    browser.close()
    assert not failures, "Падіння:\n" + "\n".join(failures)