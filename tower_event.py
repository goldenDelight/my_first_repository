from selenium.common.exceptions import (TimeoutException,
                                        StaleElementReferenceException,
                                        ElementClickInterceptedException,
                                        NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import nav
import utilities
from custom_exceptions import ShopBreakException


def grind(driver):

    if driver.bot.page() == '/mypage/index':
        nav.event_page(driver)
    elif driver.bot.page() == '/item/item_shop':
        raise ShopBreakException

    if driver.bot.page() == '/tower/tower_event_top':
        try:
            driver.find_element_by_id('canvas').click()

        except NoSuchElementException:
            try:
                stage_info = driver.execute_script("return "
                                                   "document"
                                                   ".getElementsByClassName("
                                                   "'stage_info_frame');")
                if stage_info is not None:
                    info_text = stage_info[0].text
                    info_lines = info_text.splitlines()
                    points_str = info_lines[2]
                    points_int: int = points_str.split()[-1]

                    taba_bot.print_temp(f"points: {points_int:,}")

                    if points_int >= 8000000:
                        raise ShopBreakException
            except Exception:
                pass

    if driver.bot.page() == '/tower/tower_event_top':
        try:
            driver.find_element_by_id('canvas').click()
        except NoSuchElementException:
            pass

        stage = driver.execute_script("return document.querySelector("
                                      "'#event_menu_2 > div:nth-child(3) > "
                                      "a');")
        driver.execute_script("arguments[0].click();", stage)
        WebDriverWait(driver, 3).until(ec.staleness_of(stage))

    elif driver.bot.page() == '/item/item_shop':
        raise ShopBreakException

    if driver.bot.page() == '/tower/tower_start':
        try:
            WebDriverWait(driver, 2).until(
                ec.visibility_of_all_elements_located((By.ID, 'modal-win')))
            utilities.use_stam(driver, tower_event=True)
        except TimeoutException:
            driver.bot.click('class', 'quest_dash_button')

    elif driver.bot.page() == '/item/item_shop':
        raise ShopBreakException

    if driver.bot.page() == '/tower/tower_event_result':
        try:
            driver.find_element_by_id('canvas').click()
        except NoSuchElementException:
            try:
                driver.bot.click('class', 'decision_button_column_1')
            except StaleElementReferenceException:
                pass
        try:
            driver.find_element_by_id('canvas').click()
        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass
        except ElementClickInterceptedException:
            pass

    elif driver.bot.page() == '/item/item_shop':
        raise ShopBreakException

    if driver.bot.page() == '/card/card_max':
        utilities.sell_cards(driver)
    elif driver.bot.page() == '/item/item_shop':
        raise ShopBreakException

