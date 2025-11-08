from APP.pages.basepage import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators
        self.add_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("adicionar e continuar comprando")')
        self.remove_modal = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Fechar modal carrinho")')
        self.click_cart = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Carrinho")')
        self.cart_product_name = (AppiumBy.ACCESSIBILITY_ID, 'Apple MacBook Air 13, M2, cpu de 8 núcleos, gpu de 8 núcleos, 16GB ram, 256GB ssd- Meia-noite')
        self.cart_price = (AppiumBy.ACCESSIBILITY_ID, 'De R$ 20.993,04\nPor R$ 19.438,00')
        self.proceed_to_checkout = (AppiumBy.ACCESSIBILITY_ID, 'fechar pedido\nR$ 19.438,00')
        self.zip_code = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Digite o CEP")')
        self.calculate_shipping = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Calcular")')
        self.delete_zip = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Apagar cep pesquisado")')
        self.invalid_zip = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Snackbar alerta")') 
        self.validate_email_name = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Informe seu e-mail para continuar")')

    # Click the add button
    def click_add_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.add_button))
        add = self.driver.find_element(*self.add_button)
        add.click()

    # Click the remove modal button
    def click_remove_modal(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.remove_modal))
        remove = self.driver.find_element(*self.remove_modal)
        remove.click()

    # Click the cart button
    def click_cart_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.click_cart))
        cart = self.driver.find_element(*self.click_cart)
        cart.click()
    
    # Check if the total product value and the order subtotal are double the unit price.
    def check_cart_total(self):
        expected_total = 2 * 9719.00  # 19.438,00
        expected = f"{expected_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


    # Confirm that the value on the "Proceed to Checkout" button also reflects the total for two units.
    def check_proceed_to_checkout_button(self):
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.proceed_to_checkout))
        button = self.driver.find_element(*self.proceed_to_checkout)

        # texto content-desc
        content_desc = button.get_attribute("content-desc")
        assert content_desc, "Não foi possível capturar o texto do botão 'fechar pedido'."

        normalized = content_desc.lower().replace(" ", "").replace(".", "").replace(",", ".")
        expected_total = 2 * 9719.00  # 19.438,00
        expected = f"{expected_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")  # "19.438,00"
        assert expected.replace(".", "").replace(",", ".") in normalized, (f"Valor incorreto no botão. Esperado: {expected}, encontrado: {content_desc}")

    # Enter an invalid ZIP code
    def enter_invalid_zip_code(self):
        cep_element = self.wait_for_visibility_of_element(*self.zip_code)
        cep_element.clear()
        cep_element.click()
        cep_element.send_keys("00000-000")
        calc = self.driver.find_element(*self.calculate_shipping)
        calc.click()
    
    # message error
    def message(self):
        error_message = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.invalid_zip))
        error_message = self.wait_for_visibility_of_element(*self.invalid_zip)
        return error_message is not None

    # Enter a valid ZIP code
    def enter_valid_zip_code(self):
        cep_delete = self.wait_for_visibility_of_element(*self.delete_zip)
        cep_delete.click()
        element_cep = self.wait_for_visibility_of_element(*self.zip_code)
        element_cep.click()
        element_cep.send_keys("50030-230")
        calculate = self.driver.find_element(*self.calculate_shipping)
        calculate.click()

    # Close product
    def close_product(self):
        close_element = self.wait_for_visibility_of_element(*self.proceed_to_checkout)
        close_element.click()

    # Validate email name
    def validate_email(self):
        email_element = self.wait_for_visibility_of_element(*self.validate_email_name)
        return email_element is not None