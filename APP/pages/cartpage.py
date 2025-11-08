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
        self.cart_product_macbook = (AppiumBy.ACCESSIBILITY_ID, 'Apple MacBook Air 13, M2, cpu de 8 núcleos, gpu de 8 núcleos, 16GB ram, 256GB ssd- Meia-noite')
        self.cart_price_macbook = (AppiumBy.ACCESSIBILITY_ID, 'De R$ 20.993,04\nPor R$ 19.438,00')
        self.cart_price_iPhone = (AppiumBy.ACCESSIBILITY_ID, 'Cor: Preto\nR$ 25.917,60')
        self.cart_price_watch = (AppiumBy.ACCESSIBILITY_ID, 'De R$ 13.541,04\nPor R$ 12.538,00')
        self.proceed_to_checkout = (AppiumBy.ACCESSIBILITY_ID, 'fechar pedido\nR$ 57.893,60')
        self.zip_code = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Digite o CEP")')
        self.calculate_shipping = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Calcular")')
        self.delete_zip = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Apagar cep pesquisado")')
        self.invalid_zip = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Snackbar alerta")') 
        self.validate_email_name = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Informe seu e-mail para continuar")')

    # Click the add button
    def click_add_button(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.add_button))
        add = self.driver.find_element(*self.add_button)
        add.click()

    # Click the remove modal button
    def click_remove_modal(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.remove_modal))
        remove = self.driver.find_element(*self.remove_modal)
        remove.click()

    # Click the cart button
    def click_cart_button(self):
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(self.click_cart))
        cart = self.driver.find_element(*self.click_cart)
        cart.click()
    
    # Check if the total product value and the order subtotal are double the unit price.
    def check_cart_total(self):
        expected_total_macbook = 2 * 9719.00
        expected_total_iphone = 2 * 12958.80
        expected_total_watch = 2 * 6269.00

        expected_macbook = f"{expected_total_macbook:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        expected_iphone = f"{expected_total_iphone:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        expected_watch = f"{expected_total_watch:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        # tenta pegar macbook e iphone direto
        price_macbook = self.driver.find_element(*self.cart_price_macbook).get_attribute("content-desc").replace("\xa0", " ")
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(self.cart_price_iPhone))
        price_iphone = self.driver.find_element(*self.cart_price_iPhone).get_attribute("content-desc").replace("\xa0", " ")

        # tenta o watch com scroll leve até achar
        for _ in range(3):
            try:
                price_watch = self.driver.find_element(*self.cart_price_watch).get_attribute("content-desc").replace("\xa0", " ")
                break
            except:
                self.driver.swipe(500, 1100, 500, 900, 200)
        else:
            raise AssertionError("Não foi possível encontrar o Watch no carrinho.")

        # validações
        assert expected_macbook in price_macbook, f"MacBook errado. Esperado: {expected_macbook}, Obtido: {price_macbook}"
        assert expected_iphone in price_iphone, f"iPhone errado. Esperado: {expected_iphone}, Obtido: {price_iphone}"
        assert expected_watch in price_watch, f"Watch errado. Esperado: {expected_watch}, Obtido: {price_watch}"

    # Confirm that the value on the "Proceed to Checkout" button also reflects the total for two units.
    def check_proceed_to_checkout_button(self):
        WebDriverWait(self.driver, 15).until(EC.presence_of_element_located(self.proceed_to_checkout))
        button = self.driver.find_element(*self.proceed_to_checkout)

        content_desc = button.get_attribute("content-desc")
        assert content_desc, "Não foi possível capturar o texto do botão 'Fechar pedido'."

        # Facilitar comparação
        normalized = (content_desc.lower().replace("r$", "").replace(" ", "").replace("\xa0", "").replace(".", "").replace(",", "."))

        # Totais esperados
        total_macbook = 2 * 9719.00
        total_iphone = 2 * 12958.80
        total_watch = 2 * 6269.00

        expected_total = total_macbook + total_iphone + total_watch  # soma geral

        expected_str = f"{expected_total:.2f}".replace(",", ".")

        assert expected_str in normalized, (f"Valor incorreto no botão. Esperado: R$ {expected_total:,.2f}, encontrado: {content_desc}")

    # Scroll to the zip code input
    def scroll_to_zip_code_input(self):
        try:
            self.driver.swipe(500, 1400, 500, 700, 400)  # scroll down
            zip_delete = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.delete_zip))
            zip_delete.click()
        except:
            print("delete_zip não encontrado, tentando focar direto no campo de CEP...")


    # Enter an invalid ZIP code
    def enter_invalid_zip_code(self):
        zip_delete = self.wait_for_visibility_of_element(*self.delete_zip)
        zip_delete.click()
        cep_element = self.wait_for_visibility_of_element(*self.zip_code)
        cep_element.clear()
        cep_element.click()
        cep_element.send_keys("00000000")
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
        element_cep.send_keys("50710330")
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