from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class InventoryPage(BasePage):
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    
    def get_product_add_button(self, product_name):
        product_name_normalized = product_name.lower().replace(" ", "-")
        return (By.ID, f"add-to-cart-{product_name_normalized}")
    
    def add_product_to_cart(self, product_name):
        button_locator = self.get_product_add_button(product_name)
        self.click_element(button_locator)
    
    def get_cart_badge_count(self):
        try:
            return self.get_text(self.CART_BADGE)
        except:
            return "0"
    
    def open_cart(self):
        self.click_element(self.CART_LINK)
    
    def is_on_inventory_page(self):
        return self.is_element_visible(self.INVENTORY_CONTAINER)