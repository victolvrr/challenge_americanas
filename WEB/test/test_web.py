import time
import pytest
from WEB.pages.homepage import HomePage
from WEB.pages.generatepage import GeneratePage
import pyperclip
import selenium.webdriver.support.expected_conditions as EC

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
    # Paste the temporary email into the email field
    generate_page.paste_email()
    # Click the send button
    generate_page.click_send_button()
    # Back to the generate page
    driver.switch_to.window(driver.window_handles[1])
    code = generate_page.get_verification_code()
    # time.sleep(5)
    print(f"Código de verificação capturado: {code}")
    # Back to the login tab
    driver.switch_to.window(driver.window_handles[0])
    # Paste the verification code
    generate_page.paste_verification_code()
    # time.sleep(5)
    # Click the confirm button
    generate_page.confirm_verification_code()
    # time.sleep(5)
    home_page.wait.until(EC.title_contains("Americanas"))
    assert "Americanas" in driver.title
    # Remove banner if exists
    home_page.remove_banner()
    # Check if the new user's email is displayed in the page header
    header_text = home_page.get_header_text()
    assert "olá, " in header_text
    # Click on header
    home_page.click_on_header()
    time.sleep(5)