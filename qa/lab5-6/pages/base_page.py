from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import TIMEOUTS

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.driver.implicitly_wait(TIMEOUTS["implicit_wait"])
        self.wait = WebDriverWait(driver, TIMEOUTS["explicit_wait"])
    
    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))
    
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        return self.find_element(locator).text
    
    def get_current_url(self):
        return self.driver.current_url
    
    def is_element_visible(self, locator):
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
            return False