from APP.pages.basepage import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WatchPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators
        self.search_input = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(0)')
        self.click_watch = (AppiumBy.ACCESSIBILITY_ID, '-7%\nApple Watch Series 10 gps + Cellular Caixa prateada de alumínio – 46 mm Pulseira esportiva denim – m/g\n R$ 6.770,52\nR$ 6.269,00\nà vista')
        self.watch_name = (AppiumBy.ACCESSIBILITY_ID, 'Apple Watch Series 10 gps + Cellular Caixa prateada de alumínio – 46 mm Pulseira esportiva denim – m/g')
        self.watch_price = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("R$ 6.269,00")')
        self.assert_watch = (AppiumBy.ACCESSIBILITY_ID, 'Apple Watch Series 10 gps + Cellular Caixa prateada de alumínio – 46 mm Pulseira esportiva denim – m/g\nDe R$ 6.770,52\nPor R$ 6.269,00')

    # Send keys to search input
    def send_watch(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.search_input))
        self.send_keys_to_element(*self.search_input, "Apple Watch Series 10 gps + Cellular Caixa prateada de alumínio - 46 mm Pulseira esportiva denim - m/g")

    # Click on Apple Watch
    def click(self):
        click_watch = self.wait_for_visibility_of_element(*self.click_watch)
        click_watch.click()

    # Get Apple Watch title
    def get_watch_title(self):
        element = self.wait_for_visibility_of_element(*self.watch_name)
        return element.get_attribute("content-desc")
    
    # Get Apple Watch price
    def get_watch_price(self):
        element = self.wait_for_visibility_of_element(*self.watch_price)
        return element.get_attribute("content-desc")

    # Validate product
    def assert_watch_in_cart(self):
        product_element = self.wait_for_visibility_of_element(*self.assert_watch)
        return product_element.get_attribute("content-desc")