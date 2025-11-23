from selenium.webdriver.common.by import By
from qa.lab56.pages.base_page import BasePage

class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")
    CART_ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    
    def get_cart_items_count(self):
        try:
            items = self.find_elements(self.CART_ITEMS)
            return len(items)
        except:
            return 0
    
    def get_cart_item_names(self):
        items = self.find_elements(self.CART_ITEM_NAME)
        return [item.text for item in items]
    
    def proceed_to_checkout(self):
        self.dismiss_alert_if_present()
        self.click_element(self.CHECKOUT_BUTTON)
        self.dismiss_alert_if_present()