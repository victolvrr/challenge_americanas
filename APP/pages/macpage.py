from APP.pages.basepage import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class MacBookPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators
        self.macbook_click = (AppiumBy.ACCESSIBILITY_ID, "-7%\nApple MacBook Air 13, M3, cpu de 8 núcleos, gpu de 8 núcleos, 24GB ram, 512GB ssd - Meia-noite\n R$ 18.866,52\nR$ 17.469,00\nà vista")
        self.macbook_title = (AppiumBy.ACCESSIBILITY_ID, "Apple MacBook Air 13, M3, cpu de 8 núcleos, gpu de 8 núcleos, 24GB ram, 512GB ssd - Meia-noite")
        self.macbook_price = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("R$ 17.469,00")')
        self.cep_find = (AppiumBy.ACCESSIBILITY_ID, "Simular Frete")
        self.cep_input = (AppiumBy.CLASS_NAME, "android.widget.EditText")
        self.calculate = (AppiumBy.ACCESSIBILITY_ID, "Calcular")
        self.invalid_cep = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Snackbar alerta")')
        self.valid_cep = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Receba em até 11 dias úteis: R$ 88,77")')
        self.buy_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Comprar agora")')
        self.delete_cep = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Apagar cep pesquisado")')
        self.assert_cart = (AppiumBy.ACCESSIBILITY_ID, "Apple MacBook Air 13, M3, cpu de 8 núcleos, gpu de 8 núcleos, 24GB ram, 512GB ssd - Meia-noite\nDe R$ 18.866,52\nPor R$ 17.469,00")
        self.increase_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Aumentar quantidade em 1")')
        self.decrease_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("Reduzir quantidade em 1")')
        self.quantity_field = (AppiumBy.CLASS_NAME, "android.widget.EditText")

    # click MacBook
    def click_macbook(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.macbook_click))
        click = self.driver.find_element(*self.macbook_click)
        click.click()

    # Get MacBook title
    def get_macbook_title(self):
        element = self.wait_for_visibility_of_element(*self.macbook_title)
        return element.get_attribute("content-desc")

    # Get MacBook price
    def get_macbook_price(self):
        element = self.wait_for_visibility_of_element(*self.macbook_price)
        return element.get_attribute("content-desc")

    # Scroll to a specific element
    def scroll_to_element(self, locator):
        try:
            desc = locator[1]
            ui = ('new UiScrollable(new UiSelector().scrollable(true)).setAsVerticalList()'f'.scrollForward().scrollIntoView(new UiSelector().descriptionContains("{desc}"))')
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, ui)
        except Exception:
            pass

    # Enter an invalid ZIP code
    def enter_invalid_zip_code(self):
        cep_element = self.wait_for_visibility_of_element(*self.cep_input)
        cep_element.clear()
        cep_element.click()
        cep_element.send_keys("00000-000")
        calc = self.driver.find_element(*self.calculate)
        calc.click()
    
    # message error
    def message(self):
        error_message = WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located(self.invalid_cep))
        error_message = self.wait_for_visibility_of_element(*self.invalid_cep)
        return error_message is not None

    # Enter a valid ZIP code
    def enter_valid_zip_code(self):
        cep_delete = self.wait_for_visibility_of_element(*self.delete_cep)
        cep_delete.click()
        element_cep = self.wait_for_visibility_of_element(*self.cep_input)
        element_cep.click()
        element_cep.send_keys("12345-678")
        calculate = self.driver.find_element(*self.calculate)
        calculate.click()

    # Check for success message
    def success_message(self):
        success_message = self.wait_for_visibility_of_element(*self.valid_cep)
        return success_message is not None

    # Buy MacBook
    def buy_macbook(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.buy_button))
        buy = self.driver.find_element(*self.buy_button)
        buy.click()

    # assert product name and price in cart
    def assert_product_in_cart(self):
        product_element = self.wait_for_visibility_of_element(*self.assert_cart)
        return product_element.get_attribute("content-desc")
    
    def get_quantity_value(self):
        element = self.wait_for_visibility_of_element(*self.quantity_field)
        return int(element.get_attribute("text"))
    
    # Increase the quantity to 2 and check if the quantity field is updated.
    def increase_quantity(self):
        increase = self.driver.find_element(*self.increase_button)
        increase.click()
        assert self.get_quantity_value() == 2

    # Decrease the quantity to 1 and check if the decrease button (- ) becomes inactive.
    def decrease_quantity(self):
        decrease = self.driver.find_element(*self.decrease_button)
        decrease.click()
        assert self.get_quantity_value() == 1

    # Increase the quantity to 2 again.
    def increase_quantity_again(self):
        increase = self.driver.find_element(*self.increase_button)
        increase.click()