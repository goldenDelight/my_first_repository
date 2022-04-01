import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    JavascriptException, NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

import nav
import taba_bot

xp_card_png = 'https://cf.tna.dmmgames.com/img/common/card/S/C00040b' \
              '.73fcabcb223e0a96e48159015766757a.png '


# batch sells 'N' class cards
def sell_cards(driver):
    from selenium.webdriver.support.select import Select

    # open sell/exchange page
    WebDriverWait(driver, 4).until(
        ec.presence_of_all_elements_located((
            By.CLASS_NAME, 'decision_button_column_1')))
    sell_btn = driver.find_elements_by_class_name('decision_button_column_1')

    for b in sell_btn:
        if "Sell" in b.text:
            driver.execute_script("arguments[0].click();", b)

    # batch select all N-tier cards
    WebDriverWait(driver, 4).until(
        ec.presence_of_all_elements_located((By.ID, 'card_image')))
    rarity_dropdown = driver.find_element_by_id('select_filter_rare')
    Select(rarity_dropdown).select_by_index(1)
    driver.bot.click('id', 'button_bulk')

    keep_xp(driver)

    driver.bot.click('id', 'button_sell_confirm')
    driver.bot.click('id', 'button_sell_result')

    nav.main_page(driver)


# removes xp cards from the sell group
def keep_xp(driver):
    WebDriverWait(driver, 4).until(
        ec.presence_of_all_elements_located((By.ID, 'material_card_image')))

    frames = driver.execute_script(
        "return document.querySelectorAll('[id^=showcase_frame_]');")
    for card in frames:
        try:
            card_tn = card.find_element_by_id('material_card_image')
            tn_src = card_tn.get_attribute('src')

            if tn_src == xp_card_png:
                remove = card.find_element_by_id('material_card_close')
                driver.execute_script('arguments[0].click();', remove)
                keep_xp(driver)
        except StaleElementReferenceException:
            break


def use_stam(driver, tower_event=False):
    from selenium.common.exceptions import TimeoutException

    if tower_event:
        dropdown = Select(WebDriverWait(driver, 3).until(
            ec.presence_of_element_located((By.TAG_NAME, 'select'))))
        try:
            dropdown.select_by_index(1)
        except NoSuchElementException:
            dropdown.select_by_index(0)

    try:
        WebDriverWait(driver, 3).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        use_pots = driver.execute_script(
            "return document.querySelector('a[href*=use_confirm]')")
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", use_pots)
        WebDriverWait(driver, 3).until(ec.staleness_of(use_pots))
    except TimeoutException:
        taba_bot.my_traceback()
    time.sleep(0.5)
    time.sleep(1.5)
    try:
        WebDriverWait(driver, 3).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        confirm = driver.execute_script(
            "return document.querySelector('a[href*=use_action]')")
        driver.execute_script("arguments[0].click();", confirm)
    except TimeoutException:
        taba_bot.my_traceback()

    try:
        driver.bot.click('class', 'back_button_column_1')

    except (TimeoutException, StaleElementReferenceException):
        taba_bot.my_traceback()
    WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.ID, 'loader')))
    time.sleep(0.5)


def do_bp(driver, is_event):
    try:
        pots = driver.execute_script('return document.querySelector('
                                     '\'#modal-win-inner > div > div > '
                                     'div:nth-child(7) > div:nth-child(4) > '
                                     'form > div:nth-child(2) > '
                                     'div:nth-child(1)\');')
        selector = Select(driver.find_element_by_class_name('selector'))
        owned = int(pots.text.split()[-1])

        if not is_event:
            selector.select_by_value("1")
            taba_bot.print_temp(f"{owned - 1} small bp pots left", False)
            driver.bot.click('class', 'decision_button_column_2')
        elif is_event:
            if "6" in selector.first_selected_option.text:
                driver.bot.click('id', 'IT007')
                frame = driver.execute_script(
                    "return document.querySelector('.free_frame02_mid');")
                owned_pots = int(frame.text.split()[-1])
                pots_left = owned_pots - 1
                taba_bot.print_temp(f"{pots_left} full bp pots left", False)
            else:
                taba_bot.print_temp(f"{owned - 6} bp pots left", False)
                driver.bot.click('class', 'decision_button_column_2')
        driver.bot.click('class', 'decision_button_column_2')
        driver.bot.click('class', 'back_button_column_1')
    except JavascriptException:
        taba_bot.my_traceback()


def card_limit_popup(driver):
    # list of 'button' elements by css selector
    decision_buttons_list = driver.execute_script(
        "return document.querySelectorAll('.decision_button_column_1')")

    # iterate thru text of each button
    # clicks one called 'Sell Cards'
    for label in decision_buttons_list:
        if "Sell Cards" in label.text:
            driver.execute_script("arguments[0].click();", label)


def use_pot(driver):
    print("using pot\r")
    try:
        small_pot = driver.execute_script(
            "return document.querySelector('a[href*=use_confirm]');")
        driver.execute_script("arguments[0].click();", small_pot)

        WebDriverWait(driver, 3).until(ec.staleness_of(small_pot))

        small_pot = driver.execute_script(
            "return document.querySelector('a[href*=use_action]');")
        driver.execute_script("arguments[0].click();", small_pot)

        WebDriverWait(driver, 3).until(ec.staleness_of(small_pot))

        return_ = driver.execute_script(
            "return document.querySelector('.back_button_column_1');")
        driver.execute_script("arguments[0].click();", return_)

        WebDriverWait(driver, 3).until(ec.staleness_of(return_))

    except AttributeError:
        taba_bot.my_traceback()
        return False

    return True


def restore_stam(self):
    use_small_stams = self.execute_script(
        'return document.querySelectorAll(\'.decision_button_column_2')
    self.execute_script("arguments[0].click();", use_small_stams[0])

    WebDriverWait(self, 3).until(ec.staleness_of(use_small_stams))

    confirm_use = self.find_element_by_css_selector(
        '#main_frame_item > div:nth-child(5) > a:nth-child(1)')
    self.execute_script("arguments[0].click();", confirm_use)

    WebDriverWait(self, 3).until(ec.staleness_of(confirm_use))

    return_to_event = self.find_element_by_css_selector(
        '#main_frame_item > div:nth-child(5) > a:nth-child(1)')
    self.execute_script("arguments[0].click();", return_to_event)

    WebDriverWait(self, 3).until(ec.staleness_of(return_to_event))

#     locate, click last button to return to grind_routine
    all_anchors = self.execute_script("return document.querySelectorAll('a');")
    for a in all_anchors:
        href = a.get_attribute('href')
        if '/tower/tower_start' in href:
            self.execute_script("arguments[0].click();", a)


def card_sales(driver):
    driver.execute_script("return document.querySelector('#numbner_of_card');")
    bulk = driver.execute_script("return document.querySelector('#button_bulk');")
    driver.execute_script("arguments[0].click();", bulk)


def screen_cards(driver):
    cards_to_sell = driver.execute_script("return document.querySelectorAll('div[id^=showcase_frame]');")

    for card in cards_to_sell:
        info = driver.execute_script("return arguments[0].querySelectorAll('*');", card)
        for i in info:
            if i.get_attribute('src') == 'https://cf.tna.dmmgames.com/img/common/card/S/C00040b.' \
                                         '73fcabcb223e0a96e48159015766757a.png':
                print(i.get_attribute('id'))
                print(cards_to_sell.index(card))