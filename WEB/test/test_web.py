import time
import pytest
from WEB.pages.homepage import HomePage
from WEB.pages.generatepage import GeneratePage

def test_search_functionality(driver):
    home_page = HomePage(driver)
    generate_page = GeneratePage(driver)

    # Navigate to the home page
    home_page.go_to_homepage()
    # Verify that the page title contains "Americanas"
    assert "Americanas" in driver.title
    # Navigate to the login page
    home_page.go_to_login()
    # Verify that the URL contains "login"
    assert "login" in driver.current_url
    # Open a new tab and navigate to the generate page
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    generate_page.go_to_generate_page()
    # Verify that the page title contains "Temp Mail"
    assert "Temp Mail" in driver.title
    # Generate a temporary email
    generate_page.generate_temp_email()
    # Back to the login tab
    driver.switch_to.window(driver.window_handles[0])
    # Verify we are back on login page
    assert "login" in driver.current_url