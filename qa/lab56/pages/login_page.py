from selenium.webdriver.common.by import By
from qa.lab56.pages.base_page import BasePage

class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def open(self, url):
        self.driver.get(url)
    
    def login(self, username, password):
        self.enter_text(self.USERNAME_INPUT, username)
        self.dismiss_alert_if_present()
        self.enter_text(self.PASSWORD_INPUT, password)
        self.dismiss_alert_if_present()
        self.click_element(self.LOGIN_BUTTON)
        self.dismiss_alert_if_present()
    
    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)