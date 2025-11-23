from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    
    def fill_checkout_info(self, first_name, last_name, postal_code):
        self.enter_text(self.FIRST_NAME_INPUT, first_name)
        self.enter_text(self.LAST_NAME_INPUT, last_name)
        self.enter_text(self.POSTAL_CODE_INPUT, postal_code)
    
    def click_continue(self):
        self.click_element(self.CONTINUE_BUTTON)
    
    def click_finish(self):
        self.click_element(self.FINISH_BUTTON)
    
    def get_success_message(self):
        return self.get_text(self.COMPLETE_HEADER)
    
    def is_order_complete(self):
        return self.is_element_visible(self.COMPLETE_HEADER)