import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    JavascriptException, NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

import nav
import web_driver

xp_card_thumb = "https://cf.tna.dmmgames.com/img/common/card/S/C00040b.73fcabcb223e0a96e48159015766757a.png"


# batch sells 'N' class cards
def sell_cards(driver):
    from selenium.webdriver.support.select import Select

    # open sell/exchange page
    WebDriverWait(driver, 4).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "decision_button_column_1")))
    sell_cards_btn = driver.find_elements_by_class_name("decision_button_column_1")

    for b in sell_cards_btn:
        if "Sell" in b.text:
            driver.execute_script("arguments[0].click();", b)

    # batch select all N-tier cards
    WebDriverWait(driver, 4).until(ec.presence_of_all_elements_located((By.ID, "card_image")))
    rarity_dropdown = driver.find_element_by_id("select_filter_rare")
    Select(rarity_dropdown).select_by_index(1)
    driver.click("id", "button_bulk")

    keep_xp(driver)

    driver.click('id', 'button_sell_confirm')
    driver.click('id', 'button_sell_result')

    nav.main_page(driver)


# removes xp cards from the sell group
def keep_xp(driver):
    WebDriverWait(driver, 4).until(ec.presence_of_all_elements_located((By.ID, "material_card_image")))

    frames = driver.execute_script("return document.querySelectorAll('[id^=showcase_frame_]');")
    for card in frames:
        try:
            card_tn = card.find_element_by_id("material_card_image")
            tn_src = card_tn.get_attribute("src")

            if tn_src == xp_card_thumb:
                remove = card.find_element_by_id("material_card_close")
                driver.execute_script("arguments[0].click();", remove)
                keep_xp(driver)
        except StaleElementReferenceException:
            break


# def confirm_sale(driver):
#     time.sleep(1)
#     # confirm_sale = admin.webdriver.execute_script(
#     #     "return document.getElementById('button_sell_confirm');")
#     e = driver.wait_for('id', 'button_sell_confirm')
#     # time.sleep(1)
#     driver.execute_script("arguments[0].click();", e)
#
#     e = driver.wait_for('xpath', '//*[@id="button_sell_result"]')
#     driver.execute_script("arguments[0].click();", e)
#
#     # admin.webdriver.wait_for('class', 'decision_button_column_2').click()


# def exit_sale(driver):
#     try:
#         # result = admin.webdriver.execute_script(
#         #     "return document.getElementById('button_sell_result');")
#         # admin.webdriver.execute_script("arguments[0].click();", result)
#
#         e = driver.wait_for('id', 'button_sell_result')
#         driver.execute_script("arguments[0].click();", e)
#
#     except WebDriverException:
#         web_driver.tb()
#         print_temp('no cards to sell :(')
#     # admin.webdriver.wait_for('id', 'button_sell_result').click()


def use_stam(driver, tower_event=False):
    from selenium.common.exceptions import TimeoutException

    if tower_event:
        dropdown = Select(WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.TAG_NAME, "select"))))
        try:
            dropdown.select_by_index(1)
        except NoSuchElementException:
            dropdown.select_by_index(0)

    try:
        WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located((By.TAG_NAME, "a")))
        use_pots = driver.execute_script("return document.querySelector('a[href*=use_confirm]')")
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", use_pots)
        WebDriverWait(driver, 3).until(ec.staleness_of(use_pots))
    except TimeoutException:
        web_driver.tb()
    time.sleep(0.5)
    # load_screen = WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "loader")))
    # WebDriverWait(driver, 5).until(ec.staleness_of(load_screen))
    time.sleep(1.5)
    try:
        WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located((By.TAG_NAME, "a")))
        confirm = driver.execute_script("return document.querySelector('a[href*=use_action]')")
        driver.execute_script("arguments[0].click();", confirm)
        # WebDriverWait(driver, 3).until(ec.staleness_of(confirm))
    except TimeoutException:
        web_driver.tb()

    # load_screen = WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.ID, "loader")))
    # WebDriverWait(driver, 3).until(ec.staleness_of(load_screen))

    try:
        driver.click("class", "back_button_column_1")

    except (TimeoutException, StaleElementReferenceException):
        web_driver.tb()
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "loader")))
    load_screen = driver.execute_script("return document.getElementById('loader');")
    time.sleep(0.5)
    # WebDriverWait(driver, 5).until(ec.staleness_of(load_screen))


def do_bp(driver, slayer_event):
    try:
        pots = driver.execute_script("return document.querySelector('#modal-win-inner > div > div > div:nth-child(7) "
                                     "> div:nth-child(4) > form > div:nth-child(2) > div:nth-child(1)');")
        owned = int(pots.text.split()[-1])
        selector = Select(driver.find_element_by_class_name("selector"))
        if not slayer_event:
            selector.select_by_value("1")
            web_driver.print_temp(f"{owned-1} bp pots left")
        else:
            web_driver.print_temp(f"{owned-6} bp pots left", False)
        driver.click("class", "decision_button_column_2")
        driver.click("class", "decision_button_column_2")
        driver.click("class", "back_button_column_1")
    except JavascriptException:
        web_driver.tb()


def card_limit_popup(driver):
    # list of 'button' elements by css selector
    decision_buttons_list = driver.execute_script("return document.querySelectorAll('.decision_button_column_1')")    # searching by class with js css selector

    # iterate thru text of each button
    # clicks one called 'Sell Cards'
    for label in decision_buttons_list:
        if "Sell Cards" in label.text:
            driver.execute_script("arguments[0].click();", label)


def use_pot(driver):
    print("using pot\r")
    try:
        small_pot = driver.execute_script("return document.querySelector('a[href*=use_confirm]');")
        driver.execute_script("arguments[0].click();", small_pot)

        WebDriverWait(driver, 3).until(ec.staleness_of(small_pot))

        small_pot = driver.execute_script("return document.querySelector('a[href*=use_action]');")
        driver.execute_script("arguments[0].click();", small_pot)

        WebDriverWait(driver, 3).until(ec.staleness_of(small_pot))

        return_ = driver.execute_script("return document.querySelector('.back_button_column_1');")
        driver.execute_script("arguments[0].click();", return_)

        WebDriverWait(driver, 3).until(ec.staleness_of(return_))

    except AttributeError:
        web_driver.tb()
        return False

    return True


def return_to_event(driver):
    goto_event = driver.execute_script("return document.querySelector('#main_frame > a:nth-child(7)');")    # event page
    driver.execute_script("arguments[0].click();", goto_event)
    time.sleep(1)
    goto_event = driver.execute_script("return document.querySelector('#stage_choice');")   # event stage
    driver.execute_script("arguments[0].click();", goto_event)
    time.sleep(1)
    goto_event = driver.execute_script("return document.querySelector('#event_menu_2 > div:nth-child(3) > a');")    # start stage
    driver.execute_script("arguments[0].click();", goto_event)
