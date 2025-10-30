import pyperclip, re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from WEB.pages.basepage import BasePage

class ProfilePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://www.americanas.com.br/account#/profile"
        # Locators
        self.assert_email = (By.CSS_SELECTOR, "div.vtex-my-account-1-x-emailContainer")
        self.authentication_button = (By.CSS_SELECTOR, "a[href*='#/authentication']")
        self.password_button = (By.XPATH, "//div[normalize-space()='Definir senha']")
        self.code_message = (By.CSS_SELECTOR, "span.new-message.message__subject")
        self.code_input = (By.CSS_SELECTOR, "input.vtex-styleguide-9-x-input.vtex-styleguide-9-x-hideDecorators")
        self.password_input = (By.CSS_SELECTOR,"input.vtex-styleguide-9-x-input.vtex-styleguide-9-x-hideDecorators[type='password']")
        self.save_password_button = (By.XPATH, "//div[text()='Salvar senha']/ancestor::button")
        self.masked_password_div = (By.CLASS_NAME, "vtex-my-authentication-1-x-maskedPassword_content")

    def assert_email_displayed(self):
        # Espera até o container estar visível
        self.wait_visible(self.assert_email)
        # Depois procura o texto dentro
        email = self.driver.find_element(*self.assert_email).text.strip()
        assert "@" in email

    def click_authentication(self):
        self.wait_clickable(self.authentication_button).click()

    def click_password(self):
        self.wait_clickable(self.password_button).click()

    def get_verification_code(self):
        # Espera o span aparecer com o assunto do e-mail
        code_element = self.wait.until(EC.presence_of_element_located(self.code_message))
        full_text = code_element.text.strip()
        # Extrai apenas os dígitos
        code = re.findall(r"\d+", full_text)[0]
        print(f"Código capturado: {code}")
        pyperclip.copy(code)
        return code
    
    def paste_verification_code(self):
        code = pyperclip.paste()
        input_field = self.wait.until(EC.presence_of_element_located(self.code_input))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
        self.driver.execute_script("arguments[0].click();", input_field)
        self.driver.execute_script("arguments[0].focus();", input_field)
        input_field.clear()
        input_field.send_keys(code)

    # senha com menos de 8 caracteres
    def test_password_combination(self):
        input_field = self.wait.until(EC.presence_of_element_located(self.password_input))
        input_field.send_keys("short")
    # senha sem números
        input_field.clear()
        input_field.send_keys("NoNumbers")
    # senha sem letras minúsculas
        input_field.clear()
        input_field.send_keys("NONLOWERCASE123")
    # senha sem letras maiúsculas
        input_field.clear()
        input_field.send_keys("nonuppercase123")
    # senha válida
        input_field.clear()
        input_field.send_keys("ValidPassword123")
        self.wait_clickable(self.save_password_button).click()

    def assert_password_success_message(self):
        self.wait.until(EC.visibility_of_element_located(self.masked_password_div))
        assert "******************" in self.driver.page_source