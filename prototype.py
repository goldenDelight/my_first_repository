from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import nav
import utilities
from handlers import ShopBreakException


def full_power_event_grind(driver):
    from selenium.common.exceptions import NoSuchElementException

    if driver.page() == '/mypage/index':
        nav.event_page(driver)
    elif driver.page() == "/item/item_shop":
        raise ShopBreakException

    if driver.page() == '/tower/tower_event_top':
        try:
            if driver.find_element_by_id("canvas"):
                driver.find_element_by_id("canvas").click()
        except NoSuchElementException:
            pass

        stage = driver.execute_script("return document.querySelector('#event_menu_2 > div:nth-child(3) > a');")
        driver.execute_script("arguments[0].click();", stage)
        WebDriverWait(driver, 3).until(ec.staleness_of(stage))

    elif driver.page() == "/item/item_shop":
        raise ShopBreakException

    if driver.page() == '/tower/tower_start':
        try:
            WebDriverWait(driver, 2).until(ec.visibility_of_all_elements_located((By.ID, "modal-win")))
            utilities.use_stam(driver, tower_event=True)
        except TimeoutException:
            driver.click("class", "quest_dash_button")

    elif driver.page() == "/item/item_shop":
        raise ShopBreakException

    if driver.page() == "/tower/tower_event_result":
        try:
            if driver.find_element_by_id("canvas"):
                driver.find_element_by_id("canvas").click()
        except NoSuchElementException:
            try:
                driver.click("class", "decision_button_column_1")
            except StaleElementReferenceException:
                pass
        try:
            if driver.find_element_by_id("canvas"):
                driver.find_element_by_id("canvas").click()
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass

    elif driver.page() == "/item/item_shop":
        raise ShopBreakException

    if driver.page() == "/card/card_max":
        utilities.sell_cards(driver)
    elif driver.page() == "/item/item_shop":
        raise ShopBreakException

