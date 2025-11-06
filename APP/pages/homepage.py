from APP.pages.basepage import BasePage
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # Locators
        self.click_local = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_foreground_only_button")')
        self.click_notification = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_button")')
        self.click_pictures = (AppiumBy.ANDROID_UIAUTOMATOR,'new UiSelector().resourceId("com.android.permissioncontroller:id/permission_allow_foreground_only_button")')
        self.click_search = (AppiumBy.ACCESSIBILITY_ID, "busque aqui seu produto")
        self.search_input = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(0)')

    def click_local_permission(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.click_local))
        self.driver.find_element(*self.click_local).click()

    def click_notification_permission(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.click_notification))
        self.driver.find_element(*self.click_notification).click()

    def click_pictures_permission(self):
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.click_pictures))
        self.driver.find_element(*self.click_pictures).click()

    def click_search_button(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.click_search))
        self.driver.find_element(*self.click_search).click()

    def enter_search_query(self):
        WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(self.search_input))
        self.send_keys_to_element(*self.search_input, "Apple MacBook Air 13, M2, cpu de 8 núcleos, gpu de 8 núcleos, 16GB ram, 256GB ssd- Meia-noite")