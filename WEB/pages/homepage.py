from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class HomePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.url = "https://www.americanas.com.br"
        # Locators
        self.sign_up_button = (By.XPATH, "//span[normalize-space()='olá, faça seu login']")
        self.overlay = (By.CLASS_NAME, "show-element")
        self.email_field = (By.CLASS_NAME, "render-container render-route-store-login")

    def go_to_homepage(self):
        self.driver.get(self.url)
        self.wait.until(EC.title_contains("Americanas"))

    def go_to_login(self):
        self.wait.until(EC.element_to_be_clickable(self.sign_up_button))
        button = self.driver.find_element(*self.sign_up_button)
        self.driver.execute_script("arguments[0].click();", button)

    def paste_email(self, email):
        email_field = (By.ID, "email")
        self.wait.until(EC.visibility_of_element_located(email_field))
        email_input = self.driver.find_element(*email_field)
        email_input.clear()
        email_input.send_keys(email)