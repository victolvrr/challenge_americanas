from appium import webdriver
from appium.options.common import AppiumOptions
import pytest

@pytest.fixture(scope="function")
def driver():
    """Inicializa e encerra a sessão Appium para cada teste."""
    options = AppiumOptions()
    options.load_capabilities({
        "platformName": "Android",
        "appium:deviceName": "emulator-5554",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": "com.b2w.americanas",
        "appium:appActivity": "com.b2w.americanas.MainActivity"
    })

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
    yield driver
    driver.quit()
