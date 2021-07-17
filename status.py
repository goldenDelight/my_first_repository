import time

from selenium.common.exceptions import (JavascriptException, WebDriverException)
from selenium.webdriver.support.select import Select

import web_driver

reserved_pot = 0
surplus_pot = 3
pot_frame = None


def current_bp(driver):
    try:
        b = driver.execute_script(
            'return document.getElementById("top_bp_num").innerText')[0]
        if b is not None:
            return int(b)
    except JavascriptException:
        web_driver.tb()
        if driver.find_element_by_id("gadget_contents").text == 'Request Error(0)':
            driver.refresh_frame()

        return None
    except WebDriverException:
        web_driver.tb()
        web_driver.print_temp(
            "Unable to get 'innerText' of undefined or null ref.", False)


def current_bp_cd(driver):
    try:
        bp_text = driver.execute_script(
            'return document.getElementById("bp_gage_time").innerText')[-2:]
        cd = int(bp_text)
        print(f"bp cooldown: {cd % 20}")
        return cd % 20
    except JavascriptException:
        web_driver.tb()
        if driver.find_element_by_id("gadget_contents").text == 'Request Error(0)':
            driver.refresh_frame()


def current_stam(driver):
    try:
        return int(driver.execute_script(
            'return document.getElementById("stam_gage_num").innerText')[:-4])
    except JavascriptException:
        web_driver.tb()
        pass


def do_pot(driver):
    # global reserved_pot, surplus_pot
    top_css = "#scroll_content9 > div:nth-child(2)"

    top_frame = driver.wait_for("css", top_css)

    Select(driver.find(
        'class', 'selector', parent=top_frame)).select_by_value('1')
    driver.find('class', "decision_button_column_2", parent=top_frame).click()

    time.sleep(1.5)
    driver.wait_for('class', "decision_button_column_2").click()
