import pyperclip, re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from WEB.pages.basepage import BasePage

class GeneratePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://temp-mail.io/en"
        # Locators
        self.generate_button = (By.CSS_SELECTOR, '[data-qa="current-email"]')
        self.email_field = (By.NAME, "email")
        self.send_button = (By.XPATH, "//button[.//span[text()='Enviar']]")
        self.confirm_button = (By.XPATH, "//button[.//span[normalize-space()='Confirmar']]")
        self.inbox_message = (By.CSS_SELECTOR, ".message.list-complete-item.px-5.py-4.border-b")
        self.code_message = (By.XPATH, "//span[contains(text(),'Seu código de acesso é')]")
        self.code_input = (By.NAME, "token")
        self.confirm_button = (By.XPATH, "//button[.//span[normalize-space()='Confirmar']]")

    # Abrir uma nova aba e navegar para a página de geração de e-mails temporários
    def go_to_generate_page(self):
        self.driver.get(self.url)
        self.wait.until(EC.title_contains("Temp Mail"))

    # Clicar no botão para gerar um novo e-mail temporário
    def generate_temp_email(self):
        self.wait.until(EC.element_to_be_clickable(self.generate_button))
        # Clica no botão para gerar um novo e-mail temporário
        self.driver.find_element(*self.generate_button).click()
        # Espera até que o e-mail temporário seja gerado

    def paste_email(self):
        # Lê o valor do clipboard
        text = pyperclip.paste()
        # Cola no campo de e-mail
        email_input = self.wait.until(EC.presence_of_element_located(self.email_field))
        email_input.clear()
        email_input.send_keys(text)

    # Clicar no botão de enviar
    def click_send_button(self):
        self.wait.until(EC.element_to_be_clickable(self.send_button))
        send_button = self.driver.find_element(*self.send_button)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", send_button)
        self.driver.execute_script("arguments[0].click();", send_button)

    def get_verification_code(self):
        self.wait.until(EC.element_to_be_clickable(self.inbox_message)).click()
        code_element = self.wait.until(EC.presence_of_element_located(self.code_message))
        full_text = code_element.text.strip()
        # Extrai apenas os dígitos do texto
        code = re.findall(r"\d+", full_text)[0]
        print(f"Código capturado: {code}")
        pyperclip.copy(code)
        return code

    # Colar código de verificação
    def paste_verification_code(self):
        code = pyperclip.paste()
        # Espera o campo aparecer de verdade
        input_field = self.wait.until(EC.presence_of_element_located(self.code_input))
        # Garante que o elemento está visível na tela
        self.driver.execute_script("arguments[0].scrollIntoView(true);", input_field)
        # Remove possíveis overlays ou banners (executa clique forçado via JS)
        self.driver.execute_script("arguments[0].click();", input_field)
        # Dá foco direto no input
        self.driver.execute_script("arguments[0].focus();", input_field)
        # Limpa e cola o código
        input_field.clear()
        input_field.send_keys(code)


    # Confirmar código de verificação
    def confirm_verification_code(self):
        # Espera até o botão estar realmente clicável (mesmo se o banner atrapalhar)
        confirm_btn = self.wait.until(EC.element_to_be_clickable(self.confirm_button))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", confirm_btn)
        self.driver.execute_script("arguments[0].click();", confirm_btn)