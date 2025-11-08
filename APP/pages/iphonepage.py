from APP.pages.basepage import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class iPhonePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators
        self.search_box = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(5)')
        self.remove_button = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(1)')
        self.search_input = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(0)')
        self.click_iphone = (AppiumBy.ACCESSIBILITY_ID, 'Apple iPhone 16 Pro Max 1TB Titânio preto\nR$ 12.958,80\nà vista')
        self.iphone_title = (AppiumBy.ACCESSIBILITY_ID, 'Apple iPhone 16 Pro Max 1TB Titânio preto')
        self.iphone_price = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("R$ 12.958,80")')
        self.assert_cart = (AppiumBy.ACCESSIBILITY_ID, 'Apple iPhone 16 Pro Max 1TB Titânio preto\nCor: Preto\nR$ 12.958,80')

    # Search for iPhone
    def search(self):
        search_box = self.wait_for_visibility_of_element(*self.search_box)
        search_box.click()

    # X button
    def remove(self):
        remove_button = self.wait_for_visibility_of_element(*self.remove_button)
        remove_button.click()

    # Send keys to search input
    def send_keys(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.search_input))
        self.send_keys_to_element(*self.search_input, "Apple Iphone 16 Pro Max 1TB Titânio preto")

    # Click on iPhone
    def click(self):
        click_iphone = self.wait_for_visibility_of_element(*self.click_iphone)
        click_iphone.click()

    # Get iPhone title
    def get_iphone_title(self):
        element = self.wait_for_visibility_of_element(*self.iphone_title)
        return element.get_attribute("content-desc")
    
    # Get iPhone price
    def get_price(self):
        element = self.wait_for_visibility_of_element(*self.iphone_price)
        return element.get_attribute("content-desc")
    
    # Validate product
    def assert_product_in_cart(self):
        product_element = self.wait_for_visibility_of_element(*self.assert_cart)
        return product_element.get_attribute("content-desc")