from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def game_start(driver):

    driver.switch_to.parent_frame()

    WebDriverWait(driver, 10).until(
            ec.frame_to_be_available_and_switch_to_it((By.ID, "game_frame")))

    for attempt in range(5):
        try:
            WebDriverWait(driver, 3).until(
                ec.element_to_be_clickable((By.CLASS_NAME, 'game_start_over')))

            start_btn = driver.find_element(By.CLASS_NAME, 'game_start_over')
            driver.execute_script("arguments[0].click();", start_btn)
            break
        except TimeoutException:
            if driver.find_element(By.ID, 'gadget_contents').text == "Request Error(0)":
                driver.execute_script("gadgets.util.runOnLoadHandlers();")


def log_in(driver, email, password):

    email_field = password_field = None

    # click 'login' button on top bar
    login_btn = driver.find_element(By.CLASS_NAME, 'js-login')
    login_btn.click()

    # locate account email and password entry fields
    for i in driver.find_elements(By.TAG_NAME, 'input'):
        if 'email' in i.get_attribute('name'):
            email_field = i
        elif 'password' in i.get_attribute('name'):
            password_field = i

    # enter account email/password
    email_field.send_keys(email)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(ec.staleness_of(password_field))

    login_btn = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.TAG_NAME, 'form')))

    login_btn.click()
