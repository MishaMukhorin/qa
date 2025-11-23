import pytest
from selenium import webdriver
from qa.lab56.pages.login_page import LoginPage
from qa.lab56.pages.inventory_page import InventoryPage
from qa.lab56.pages.cart_page import CartPage
from qa.lab56.pages.checkout_page import CheckoutPage
from qa.lab56.config import TEST_URL, TEST_DATA

class TestUI:
    
    @pytest.fixture
    def driver(self, request):
        driver = webdriver.Chrome()
        driver.maximize_window()
        yield driver
        driver.quit()
    
    def test_authorization(self, driver):
        login_page = LoginPage(driver)
        login_page.open(TEST_URL)
        
        login_page.login(
            TEST_DATA["login"]["username"],
            TEST_DATA["login"]["password"]
        )
        
        assert driver.current_url == TEST_DATA["login"]["expected_url"]
        
        inventory_page = InventoryPage(driver)
        assert inventory_page.is_on_inventory_page()
    
    def test_search_product_in_catalog(self, driver):
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
    
    def test_add_product_to_cart(self, driver):
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
    
    def test_checkout_order(self, driver):
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