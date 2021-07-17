import re
import sys
import traceback

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    UnexpectedAlertPresentException,
    JavascriptException,
    StaleElementReferenceException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from handlers import RequestError0

search_syntax_dic = {
    "css": By.CSS_SELECTOR,
    "xpath": By.XPATH,
    "id": By.ID,
    "tag": By.TAG_NAME,
    "class": By.CLASS_NAME,
    "name": By.NAME
}

find_syntax_dic = {
    "id": (lambda a, b: a.find_element_by_id(b)),
    "tag": (lambda a, b: a.find_element_by_tag_name(b)),
    "class": (lambda a, b: a.find_element_by_class_name(b)),
    "name": (lambda a, b: a.find_element_by_name(b)),
    "css": (lambda a, b: a.find_element_by_css_selector(b))
}


def page(driver):
    return driver.execute_script("return location_url")


def bp_pot_tracker(driver, count):
    driver.bp_pot_count = count
    if driver.starting_bp_pots_count == 0:
        driver.starting_bp_pots_count = count
    return None


def click(driver, search_key, search_value):
    try:
        WebDriverWait(driver, 3).until(ec.element_to_be_clickable((search_syntax_dic.get(search_key), search_value)))
    except TimeoutException:
        pass

    try:
        get = find_syntax_dic.get(search_key)
        element = get(driver, search_value)
        driver.execute_script("arguments[0].click();", element)
        WebDriverWait(driver, 3).until(ec.staleness_of(element))
    except NoSuchElementException:
        if driver.find_element_by_id("gadget_contents").text == 'Request Error(0)':
            raise RequestError0
    except TimeoutException:
        print_temp("element not stale")

    return None


def find(driver, search_type, search_value, parent=None):
    loc = search_syntax_dic.get(search_type)
    element = driver.search_cycle(loc, search_value, parent)
    return element


def wait_for(driver, locator, value, t=5, parent=None):
    locator = search_syntax_dic.get(locator)
    parent = driver if parent is None else parent
    element = None

    try:
        element = WebDriverWait(parent, t).until(ec.element_to_be_clickable((locator, value)))
    except TimeoutException:
        try:
            element = WebDriverWait(parent, t).until(ec.visibility_of_element_located((locator, value)))
        except TimeoutException:
            pass

    return element


def find_href(driver, substring):
    href_query = "return document.querySelector('a[href*=" + substring + "]')"
    element = driver.search_cycle(href_query)
    return element


def find_substring(driver, sub_str, parent=None):
    parent = driver if parent is None else parent
    try:
        WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{sub_str}')]")))
        return parent.find_element_by_xpath(f"//*[contains(text(), '{sub_str}')]")
    except TimeoutException:
        return None


def search_cycle(driver, locator, value=None, parent=None):
    import time
    parent = driver if parent is None else parent
    for i in range(15):
        try:
            if value is None:
                return driver.execute_script(locator)
            else:
                parent.find_element(locator, value)
        except NoSuchElementException: pass
        except UnexpectedAlertPresentException: pass
        except JavascriptException: pass
        except StaleElementReferenceException: print("stale element reference exception")

        time.sleep(0.1)
    return None


def set_boss_name(driver):
    # status = driver.execute_script("return document.getElementsByClassName('quest_boss_status_1');")
    WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "quest_boss_status_1")))
    status = driver.find_elements_by_class_name("quest_boss_status_1")
    name = status[0].text
    if name is not None:
        driver.boss_name = name
    return None


def bp_cooldown(driver):
    import status
    return status.current_bp_cd(driver)


def current_bp(driver):
    import status
    return status.current_bp(driver)


def print_temp(_str, temp=True):
    import time
    linebreak = '\r' if temp else '\n'
    print(f"{time.strftime('%H:%M:%S')} {_str}", end=linebreak, flush=True)
    return None


def animated_text(stall_text, wait=13, interval=1):
    for c in range(wait):
        print(stall_text, end="\r")
        if stall_text.__len__() == 13:
            stall_text = "stalling"
        else:
            stall_text += "."
        import time
        time.sleep(interval)
    return None


def tb():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print_temp(traceback.print_exception(exc_type, exc_value, exc_traceback,
                                         limit=4, file=sys.stdout))
    return None


def get_bp_pot_count(driver):
    driver.click("class", "top_menu_7")
    btns = driver.find_elements_by_class_name("decision_button_column_2")
    driver.execute_script("arguments[0].click();", btns[2])

    WebDriverWait(driver, 4).until(ec.staleness_of(btns[2]))

    items = driver.find_elements_by_class_name("item_shop_description")
    driver.bp_pot_count = re.sub('[^0-9]', "", items[16].text)
    print(driver.bp_pot_count)

    if driver.starting_bp_pots_count is None:
        driver.starting_bp_pots_count = driver.bp_pot_count
    return None


def refresh_frame(driver):
    driver.execute_script("gadgets.util.runOnLoadHandlers();")
    import startup
    startup.game_start(driver)
    return None
