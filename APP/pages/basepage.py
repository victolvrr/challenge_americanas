from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
 
class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
 
    def find_element(self, by, locator):
        return self.driver.find_element(by, locator)
 
    # ----------------- WAITS EXPLÍCITOS -----------------
    def wait_for_visibility_of_element(self, by, locator):
        return self.wait.until(EC.visibility_of_element_located((by, locator)))
 
    def wait_for_element_to_be_clickable(self, by, locator):
        return self.wait.until(EC.element_to_be_clickable((by, locator)))
 
    def wait_for_presence_of_element(self, by, locator):
        return self.wait.until(EC.presence_of_element_located((by, locator)))
 
    # ----------------- AÇÕES COM WAITS EXPLÍCITOS -----------------
    def click_element(self, by, locator):
        """Clica em um elemento após esperar que ele esteja clicável."""
        self.wait_for_element_to_be_clickable(by, locator).click()
 
    def send_keys_to_element(self, by, locator, text, clear_first=True):
        """Preenche um campo de texto após esperar que ele esteja visível.
        Opcionalmente, limpa o campo antes de enviar o texto."""
        element = self.wait_for_visibility_of_element(by, locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
 
    def get_element_text(self, by, locator):
        """Retorna o texto de um elemento após esperar que ele esteja visível."""
        element = self.wait_for_visibility_of_element(by, locator)
        return element.text
 
    def get_element_attribute(self, by, locator, attribute):
        """Retorna o valor de um atributo de um elemento após esperar que ele esteja visível."""
        element = self.wait_for_visibility_of_element(by, locator)
        return element.get_attribute(attribute)
 
    def is_element_displayed(self, by, locator):
        """Verifica se o elemento está visível na tela."""
        try:
            return self.wait_for_visibility_of_element(by, locator).is_displayed()
        except TimeoutException:
            return False
 
    def is_element_enabled(self, by, locator):
        """Verifica se o elemento está habilitado."""
        try:
            return self.wait_for_presence_of_element(by, locator).is_enabled()
        except TimeoutException:
            return False
 
    def is_element_selected(self, by, locator):
        """Verifica se o elemento está selecionado (checkbox, radio)."""
        try:
            return self.wait_for_presence_of_element(by, locator).is_selected()
        except TimeoutException:
            return False
        
    def is_button_disabled(self, by, locator):
        """Verifica se o botão está desativado (não clicável ou desabilitado)."""
        button = self.driver.find_element(by, locator)
        enabled = button.get_attribute("enabled")
        clickable = button.get_attribute("clickable")
        return enabled == "false" or clickable == "false"

