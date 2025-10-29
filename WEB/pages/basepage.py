from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from WEB.conftest import driver

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.base_url = "https://www.americanas.com.br/"

    def open(self, url_path=""):
        self.driver.get(self.base_url + url_path)

    def wait_visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def element_exists(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except:
            return False