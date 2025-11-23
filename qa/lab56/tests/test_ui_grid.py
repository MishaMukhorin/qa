import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from qa.lab56.pages.login_page import LoginPage
from qa.lab56.pages.inventory_page import InventoryPage
from qa.lab56.pages.cart_page import CartPage
from qa.lab56.pages.checkout_page import CheckoutPage
from qa.lab56.config import TEST_URL, TEST_DATA, SELENIUM_GRID, TIMEOUTS


class TestUIGrid:

    @pytest.fixture(params=SELENIUM_GRID["browsers"], scope="function")
    def driver(self, request):
        browser = request.param

        if browser == "chrome":
            options = ChromeOptions()
            options.add_experimental_option("prefs", {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2,
                "autofill.profile_enabled": False,
                "autofill.credit_card_enabled": False,
                "autofill.enabled": False,
                "password_manager_enabled": False,
                "profile.password_manager_leak_detection": False
            })
            options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
            options.add_experimental_option('useAutomationExtension', False)
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_argument("--disable-save-password-bubble")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-notifications")

            driver = webdriver.Remote(
                command_executor=SELENIUM_GRID["hub_url"],
                options=options
            )
        elif browser == "firefox":
            options = FirefoxOptions()
            options.set_preference("signon.rememberSignons", False)
            options.set_preference("signon.autofillForms", False)
            options.set_preference("security.insecure_password.ui.enabled", False)

            driver = webdriver.Remote(
                command_executor=SELENIUM_GRID["hub_url"],
                options=options
            )
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        driver.set_page_load_timeout(TIMEOUTS["page_load"])
        driver.implicitly_wait(TIMEOUTS["implicit_wait"])
        driver.maximize_window()

        yield driver

        try:
            driver.quit()
        except:
            pass

    def test_authorization_grid(self, driver):
        login_page = LoginPage(driver)
        login_page.open(TEST_URL)

        login_page.login(
            TEST_DATA["login"]["username"],
            TEST_DATA["login"]["password"]
        )

        assert driver.current_url == TEST_DATA["login"]["expected_url"]

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_on_inventory_page()

    def test_search_product_in_catalog_grid(self, driver):
        login_page = LoginPage(driver)
        login_page.open(TEST_URL)
        login_page.login(
            TEST_DATA["login"]["username"],
            TEST_DATA["login"]["password"]
        )

        inventory_page = InventoryPage(driver)
        assert inventory_page.is_on_inventory_page()

        items = inventory_page.find_elements(inventory_page.INVENTORY_ITEMS)
        assert len(items) > 0

    def test_add_product_to_cart_grid(self, driver):
        login_page = LoginPage(driver)
        login_page.open(TEST_URL)
        login_page.login(
            TEST_DATA["login"]["username"],
            TEST_DATA["login"]["password"]
        )

        inventory_page = InventoryPage(driver)
        product_name = TEST_DATA["cart"]["product_name"]
        inventory_page.add_product_to_cart(product_name)

        cart_count = inventory_page.get_cart_badge_count()
        assert cart_count == TEST_DATA["cart"]["expected_item_count"]

    def test_checkout_order_grid(self, driver):
        login_page = LoginPage(driver)
        login_page.open(TEST_URL)
        login_page.login(
            TEST_DATA["login"]["username"],
            TEST_DATA["login"]["password"]
        )

        inventory_page = InventoryPage(driver)
        inventory_page.add_product_to_cart(TEST_DATA["cart"]["product_name"])
        inventory_page.open_cart()

        cart_page = CartPage(driver)
        assert cart_page.get_cart_items_count() == 1
        cart_page.proceed_to_checkout()

        checkout_page = CheckoutPage(driver)
        checkout_page.fill_checkout_info(
            TEST_DATA["checkout"]["first_name"],
            TEST_DATA["checkout"]["last_name"],
            TEST_DATA["checkout"]["postal_code"]
        )
        checkout_page.click_continue()
        checkout_page.click_finish()

        assert checkout_page.is_order_complete()
        success_msg = checkout_page.get_success_message()
        assert TEST_DATA["checkout"]["expected_success_message"].lower() in success_msg.lower()

