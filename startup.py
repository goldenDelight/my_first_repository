from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def game_start(driver):
    print("game start\r")

    if driver.switch_to.parent_frame():
        print("switched to parent frame\r")

    if WebDriverWait(driver, 10).until(
            ec.frame_to_be_available_and_switch_to_it((By.ID, "game_frame"))):
        print("switched to game frame\r")

    attempt = 0
    while attempt < 5:
        attempt += 1
        try:
            WebDriverWait(driver, 3).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'game_start_over')))

            start_btn = driver.find_element_by_class_name('game_start_over')
            driver.execute_script("arguments[0].click();", start_btn)
            break
        except TimeoutException:
            if driver.find_element_by_id(
                    'gadget_contents').text == "Request Error(0)":
                driver.execute_script("gadgets.util.runOnLoadHandlers();")


def log_in(driver):
    # click 'login' button on top bar
    open_login_css = '#page > header > div.flx-a-c.mar-a-l > div.user.flx-a-c > ' \
                     'span.button.outlined.white.ripple.js-btn-modal.js-login '
    driver.bot.click('css', open_login_css)

    email = None
    password = None

    # locate account email and password entry fields
    for i in driver.find_elements_by_tag_name('input'):
        if 'Email' in i.get_attribute('placeholder'):
            email = i
        elif 'Password' in i.get_attribute('placeholder'):
            password = i

    # enter account email/password
    email.send_keys("11throwaway.23@gmail.com")
    password.send_keys("skateboard")

    # submit login, close pop-up
    login_btn_css = '#page > div.modal.js-modal-signup-login.open.display-up > div > ' \
                    'div.flx.content-login.js-content-login.display-up > div > form > button '
    WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.CSS_SELECTOR, login_btn_css)))
    driver.bot.click('css', login_btn_css)

    continue_playing_btn_css = '#page > div.js-main-content.main-content.sidebar-closed > div.flx-column > ' \
                               'div.flx.cnt-product > div.cnt-product-col-right.flx-column > ' \
                               'section.box.rounded.dark.flx-column > form > button '
    WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, continue_playing_btn_css)))
    driver.bot.click('css', continue_playing_btn_css)
