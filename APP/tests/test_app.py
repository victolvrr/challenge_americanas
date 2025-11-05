import pytest
import time
from APP.pages.homepage import HomePage
from APP.pages.macpage import MacBookPage
from APP.pages.cartpage import CartPage

def test_full_purchase_flow(driver):
    # init pages
    home_page = HomePage(driver)
    macbook_page = MacBookPage(driver)
    cart_page = CartPage(driver)

    # click local permission
    home_page.click_local_permission()
    # click notification permission
    home_page.click_notification_permission()
    # click pictures permission
    home_page.click_pictures_permission()
    # click search
    home_page.click_search_button()
    home_page.enter_search_query()
    # click MacBook
    macbook_page.click_macbook()
    # validate MacBook page
    assert "Apple MacBook Air 13" in macbook_page.get_macbook_title()
    assert "R$ 17.469,00" in macbook_page.get_macbook_price()
    # scroll to cep input
    macbook_page.scroll_to_element(macbook_page.cep_find)
    # enter invalid zip code
    macbook_page.enter_invalid_zip_code()
    assert macbook_page.message() is True
    # enter valid zip code
    macbook_page.enter_valid_zip_code()
    assert macbook_page.success_message() is True
    # buy MacBook
    macbook_page.buy_macbook()
    # In the cart popup, confirm the product name and price again.
    product_info = macbook_page.assert_product_in_cart()
    product_info = product_info.replace("\xa0", " ")
    assert "Apple MacBook Air 13" in product_info
    assert "R$ 17.469,00" in product_info
    # Increase the quantity to 2 and check if the quantity field is updated.
    macbook_page.increase_quantity()
    assert macbook_page.get_quantity_value() == 2
    # Decrease the quantity to 1 and check if the decrease button (-) becomes inactive.
    macbook_page.decrease_quantity()
    # Increase the quantity to 2 again.
    macbook_page.increase_quantity_again()
    assert macbook_page.get_quantity_value() == 2
    # Click the add button
    cart_page.click_add_button()
    # Click the remove modal button
    cart_page.click_remove_modal()
    # Click the cart button
    cart_page.click_cart_button()
    # Validate the cart page
    assert "Apple MacBook Air 13" in cart_page.get_cart_product_name()
    assert "R$ 17.469,00" in cart_page.get_cart_price()
    # Check if the cart total is correct
    cart_page.check_cart_total()
    # Check if the proceed to checkout button is correct
    cart_page.check_proceed_to_checkout_button()
    # Enter an invalid ZIP code
    cart_page.enter_invalid_zip_code()
    assert cart_page.message() is True
    # Enter a valid ZIP code
    cart_page.enter_valid_zip_code()
    assert cart_page.success_message() is True
    # Close product
    cart_page.close_product_mac()
    # Validate email
    assert cart_page.validate_email_name() is True