import pytest
from selenium import webdriver
from pathlib import Path
from selenium.webdriver.chrome.options import Options as ChromeOptions

def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to run tests against"
    )

def driver(request):
    browser = request.config.getoption("--browser")
    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
    else:
        raise ValueError(f"Browser '{browser}' is not supported.")
    
    yield driver
    driver.quit(
    )

