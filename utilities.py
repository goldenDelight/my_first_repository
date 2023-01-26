import sys
import time
import traceback

from selenium.common.exceptions import (
    StaleElementReferenceException,
    JavascriptException, NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

import nav

xp = 'https://cf.tna.dmmgames.com/img/common/card/S/C00040b.73fcabcb223e0a96e48159015766757a.png'
last_message = ""


# batch sells 'N' class cards
def sell_cards(driver):
    from selenium.webdriver.support.select import Select

    # open sell/exchange page
    WebDriverWait(driver, 4).until(
        ec.presence_of_all_elements_located((
            By.CLASS_NAME, 'decision_button_column_1')))
    sell_btn = driver.find_elements(By.CLASS_NAME, 'decision_button_column_1')
    [driver.execute_script("arguments[0].click();", b) for b in sell_btn if "Sell" in b.text]

    # batch select all N-tier cards
    WebDriverWait(driver, 4).until(
        ec.presence_of_all_elements_located((By.ID, 'card_image')))

    rarity_dropdown = driver.find_element(By.ID, 'select_filter_rare')
    Select(rarity_dropdown).select_by_index(1)
    bulk = driver.find_element(By.ID, 'button_bulk')
    driver.execute_script("arguments[0].click();", bulk)

    while xp_cards := [card.find_element(By.ID, 'material_card_close')
                       for card
                       in driver.execute_script("return document.querySelectorAll('[id^=showcase_frame_]');")
                       if card.find_element(By.ID, 'material_card_image').get_attribute('src') == xp]:

        driver.execute_script('arguments[0].click();', xp_cards.pop())

    driver.bot.click('id', 'button_sell_confirm')
    driver.bot.click('id', 'button_sell_result')

    nav.main_page(driver)


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
        use_pots = lambda driver: driver.execute_script(
            "return document.querySelector('a[href*=use_confirm]')")
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", use_pots(driver))
        # WebDriverWait(driver, 3).until(ec.staleness_of(pot))
    except TimeoutException:
        my_traceback()
    time.sleep(0.5)
    time.sleep(1.5)
    try:
        WebDriverWait(driver, 3).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        confirm = lambda driver: driver.execute_script(
            "return document.querySelector('a[href*=use_action]')")
        driver.execute_script("arguments[0].click();", confirm(driver))
    except TimeoutException:
        my_traceback()
    except StaleElementReferenceException:
        use_stam(driver, tower_event)

    try:
        driver.bot.click('class', 'back_button_column_1')

    except (TimeoutException, StaleElementReferenceException):
        my_traceback()
    WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.ID, 'loader')))
    time.sleep(0.5)


def do_bp(driver, event_grind=False):
    try:
        pots = driver.execute_script('return document.querySelector('
                                     '\'#modal-win-inner > div > div > '
                                     'div:nth-child(7) > div:nth-child(4) > '
                                     'form > div:nth-child(2) > '
                                     'div:nth-child(1)\');')
        selector = Select(driver.find_element(By.CLASS_NAME, 'selector'))
        owned = int(pots.text.split()[-1])

        if event_grind is False:
            selector.select_by_value("1")
            print_temp(f"{owned - 1:,} small bp pots left", False)
            driver.bot.click('class', 'decision_button_column_2')

        elif event_grind is True:
            # if "6" in selector.first_selected_option.text:
            #     driver.bot.click('id', 'IT007')
            #     frame = driver.execute_script(
            #         "return document.querySelector('.free_frame02_mid');")
            #     owned_pots = int(frame.text.split()[-1])
            #     pots_left = owned_pots - 1
            #     taba_bot.print_temp(f"{pots_left} full bp pots left", False)
            # else:
            #     print_temp(f"{owned - 6:,} my_bp pots left", temp=False)
                driver.bot.click('class', 'decision_button_column_2')

        driver.bot.click('class', 'decision_button_column_2')
        driver.bot.click('class', 'back_button_column_1')
    except JavascriptException:
        my_traceback()


def name_is(func):
    import time

    def wrap(*args, **kwargs):
        global last_message
        result = func(*args, **kwargs)

        if f"{time.strftime('%H:%M:%S')} {func.__name__}" != last_message:
            last_message = f"{time.strftime('%H:%M:%S')} {func.__name__}"
            print(last_message, flush=True)
        return result

    return wrap


def animated_text(stall_text, wait=26, interval=1):
    for c in range(wait):
        print(stall_text, end='\r')
        if stall_text.__len__() == 13:
            stall_text = "stalling"
        else:
            stall_text += "."
        import time
        time.sleep(interval)
    return None


def print_temp(_str, temp=True):
    import time
    linebreak = '\r' if temp else '\n'
    print(f"{time.strftime('%H:%M:%S')} {_str}", end=linebreak, flush=True)
    return None


def my_traceback():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print_temp(traceback.print_exception(exc_type, exc_value, exc_traceback,
                                         limit=4, file=sys.stdout))
    return None


