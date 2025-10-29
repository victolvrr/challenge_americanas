from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from WEB.pages.basepage import BasePage

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.americanas.com.br"
        # Locators
        self.sign_up_button = (By.XPATH, "//span[normalize-space()='olá, faça seu login']")
        self.overlay = (By.CLASS_NAME, "show-element")
        self.email_field = (By.CLASS_NAME, "render-container render-route-store-login")
        self.header = (By.XPATH, "//span[contains(text(), 'olá')]")

    def go_to_homepage(self):
        self.open()
        self.wait.until(EC.title_contains("Americanas"))

    def go_to_login(self):
        self.wait.until(EC.element_to_be_clickable(self.sign_up_button))
        button = self.driver.find_element(*self.sign_up_button)
        self.driver.execute_script("arguments[0].click();", button)

    def paste_email(self, email):
        email_field = (By.ID, "email")
        self.wait_visible(email_field)
        email_input = self.driver.find_element(*email_field)
        email_input.clear()
        email_input.send_keys(email)

    def remove_banner(self):
        try:
            overlay = self.wait_clickable(self.overlay)
            overlay.click()
        except:
            print("Nenhum banner encontrado, continuando...")
    
    def is_user_logged_in(self):
        header_text = self.driver.find_element(*self.header).text
        return "olá, " in header_text

    def get_header_text(self):
        try:
            element = self.wait_visible(self.header)
            return element.text
        except:
            print("Header não apareceu a tempo")
            return ""

    def click_on_header(self):
        header = self.wait_clickable(self.header)
        self.driver.execute_script("arguments[0].click();", header)