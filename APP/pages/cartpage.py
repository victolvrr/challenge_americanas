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
        self.cart_product_name = (AppiumBy.ACCESSIBILITY_ID, 'Apple MacBook Air 13, M3, cpu de 8 núcleos, gpu de 8 núcleos, 24GB ram, 512GB ssd - Meia-noite')
        self.cart_price = (AppiumBy.ACCESSIBILITY_ID, 'De R$ 18.866,52\nPor R$ 17.469,00')
        self.proceed_to_checkout = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Fechar pedido")')
        self.zip_code = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Digite o CEP")')
        self.calculate_shipping = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Calcular")')
        self.delete_zip = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Apagar cep pesquisado")')
        self.invalid_zip = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Snackbar alerta")')
        self.valid_zip = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Receba em até 11 dias úteis: R$ 88,77")')
        self.close_product_mac = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Fechar pedido")')
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

    # Get cart product name
    def get_cart_product_name(self):
        product_name = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.cart_product_name))
        return product_name.text

    # Get cart price
    def get_cart_price(self):
        price = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.cart_price))
        return price.text
    
    # Check if the total product value and the order subtotal are double the unit price.
    def check_cart_total(self):
        unit_price = 17469.00
        total_price = 2 * unit_price
        assert total_price == self.get_cart_price(), "Total price is not double the unit price"

    # Confirm that the value on the "Proceed to Checkout" button also reflects the total for two units.
    def check_proceed_to_checkout_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.proceed_to_checkout))
        proceed_button = self.driver.find_element(*self.proceed_to_checkout)
        assert proceed_button.text == f"Total: R$ {2 * 17469.00}", "Proceed to Checkout button does not reflect the correct total"

    # Repeat the invalid and valid ZIP code test to ensure shipping calculation consistency.
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
        element_cep.send_keys("12345-678")
        calculate = self.driver.find_element(*self.calculate_shipping)
        calculate.click()

    # Check for success message
    def success_message(self):
        success_message = self.wait_for_visibility_of_element(*self.valid_zip)
        return success_message is not None

    # Close product
    def close_product(self):
        close_element = self.wait_for_visibility_of_element(*self.close_product_mac)
        close_element.click()

    # Validate email name
    def validate_email(self):
        email_element = self.wait_for_visibility_of_element(*self.validate_email_name)
        return email_element is not None