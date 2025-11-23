TEST_URL = "https://www.saucedemo.com"

TEST_DATA = {
    "login": {
        "username": "standard_user",
        "password": "secret_sauce",
        "expected_url": "https://www.saucedemo.com/inventory.html"
    },
    "search": {
        "product_name": "Sauce Labs Backpack",
        "expected_price": "$29.99"
    },
    "cart": {
        "product_name": "Sauce Labs Backpack",
        "expected_item_count": "1"
    },
    "checkout": {
        "first_name": "John",
        "last_name": "Doe",
        "postal_code": "52479",
        "expected_success_message": "Thank you for your order"
    }
}

SELENIUM_GRID = {
    "hub_url": "http://localhost:4444/wd/hub",
    "browsers": ["chrome", "firefox"]
}

TIMEOUTS = {
    "implicit_wait": 10,
    "explicit_wait": 15,
    "page_load": 30
}