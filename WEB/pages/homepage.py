from WEB.pages.basepage import BasePage
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.driver.get(self.base_url)
        # Locators
        self.sign_up_button = (By.XPATH, '//*[@id="__next"]/header/div/section[1]/div/a[2]/div[2]/span[2]')

    def click_sign_up(self):
        self.wait.until(EC.element_to_be_clickable(self.sign_up_button)).click()