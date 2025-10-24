from re import I
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

class GeneratePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.url = "https://temp-mail.io/en"
        # Locators
        self.generate_button = (By.ID, "email")
        
    # Abrir uma nova aba e navegar para a página de geração de e-mails temporários
    def go_to_generate_page(self):
        self.driver.get(self.url)
        self.wait.until(EC.title_contains("Temp Mail"))

    # Clicar no botão para gerar um novo e-mail temporário
    def generate_temp_email(self):
        self.wait.until(EC.element_to_be_clickable(self.generate_button))
        button = self.driver.find_element(*self.generate_button)
        self.driver.execute_script("arguments[0].click();", button)