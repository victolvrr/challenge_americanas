import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests against")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    
    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")
    
    driver.maximize_window()
    yield driver
    driver.quit()
