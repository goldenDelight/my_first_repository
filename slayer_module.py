import time

import selenium.webdriver.support.expected_conditions as ec
from selenium.common.exceptions import (JavascriptException,
                                        TimeoutException,
                                        NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import logic
import nav
import output
import quest
import utilities
import web_driver
from handlers import MaxCardLimitException, RequestError0, ShopBreakException


def nav_to_event_splash(driver):
    if "/hunt/hunt_event_top" not in driver.page():
        links = driver.execute_script("return document.querySelectorAll('a');")
        for link in links:
            if "hunt_event_top" in link.get_attribute('href'):
                driver.execute_script("arguments[0].click();", link)
                break


def nav_to_boss_list(driver):
    if "/hunt/raid_list" not in driver.page():
        links = driver.execute_script("return document.querySelectorAll('a');")
        for link in links:
            if "/hunt/raid_list" in link.get_attribute('href'):
                driver.execute_script("arguments[0].click();", link)
                break


def nav_to_boss(driver):
    if "/raid/boss_arrival" not in driver.page():
        links = driver.execute_script("return document.querySelectorAll('a');")
        for link in links:
            if "/raid/boss_arrival" in link.get_attribute('href'):
                driver.execute_script("arguments[0].click();", link)
                break


def nav_to_stage(driver):
    if "/hunt/hunt_start" not in driver.page():
        links = driver.execute_script("return document.querySelectorAll('a');")
        for link in links:
            if "/hunt/hunt_start" in link.get_attribute('href'):
                driver.execute_script("arguments[0].click();", link)
                break


def slayer_event(driver):
    # driver.wait_for('id', 'page_title_text')
    driver.switch_to.parent_frame()
    WebDriverWait(driver, 10).until(
        ec.frame_to_be_available_and_switch_to_it((By.ID, "game_frame")))

    if driver.page() == "/raid/boss_achievement":
        try:
            canvas = driver.execute_script(
                "return document.querySelector('#canvas');")
            canvas.click()
        except AttributeError:
            pass
    try:

        if driver.page() == "/item/item_shop":
            raise ShopBreakException

        if driver.page() == "/raid/boss_arrival":
            logic.fight(driver, slayer_event=True)
            nav.battle_to_event_stage(driver)

        elif driver.page() == "/hunt/hunt_start":
            quest.grind(driver, slayer_event=True)
            nav.quest_to_boss_list(driver, slayer_event=True)
            nav.battle_page(driver, slayer_event=True)
            logic.fight(driver, slayer_event=True)
            nav.battle_to_event_stage(driver)

        elif driver.page() == "/hunt/hunt_event_top":
            if check_for_boss(driver):
                if nav.battle_page(driver, slayer_event=True):
                    logic.fight(driver, slayer_event=True)
                    nav.battle_to_event_stage(driver)
                else:
                    nav.event_stage(driver)
                    quest.grind(driver, slayer_event=True)
                    nav.quest_to_boss_list(driver, slayer_event=True)
                    nav.battle_page(driver, slayer_event=True)
                    logic.fight(driver, slayer_event=True)
                    nav.battle_to_event_stage(driver)

            else:
                nav.event_stage(driver)
                quest.grind(driver, slayer_event=True)
                nav.quest_to_boss_list(driver, slayer_event=True)
                nav.battle_page(driver)
                logic.fight(driver, slayer_event=True)
                nav.battle_to_event_stage(driver)

        elif driver.page() == "/mypage/index":
            nav.event_page(driver)

        elif driver.page() == "/card/card_max":
            utilities.sell_cards(driver)
            nav.event_page(driver)
            check_for_boss(driver)
            nav.event_stage(driver)

        elif driver.page() == '/raid/boss_help_select':
            import battle
            battle.get_partner(driver)

    except TimeoutException:
        pass
    except JavascriptException:
        driver.switch_to.parent_frame()
        WebDriverWait(driver, 10).until(
                ec.frame_to_be_available_and_switch_to_it(
                    (By.ID, "game_frame")))



def check_for_boss(driver):
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, "a")))
        boss_list = driver.execute_script(
            "return document.querySelector('a[href*=raid_list]');")
        driver.execute_script("arguments[0].click();", boss_list)
        return True
    except TimeoutException:
        return False
    except AttributeError:
        return False
    except JavascriptException:
        return False


def grind_routine(driver):
    import nav
    import quest

    try:
        if driver.page() == "/item/item_shop":
            raise ShopBreakException

        if nav.battle_page(driver):
            nav.boss_recon(driver)

        else:
            nav.quest(driver)
            quest.grind(driver)
            nav.quest_to_boss_list(driver)
            nav.battle_page(driver)
            nav.boss_recon(driver)

    except TimeoutException:
        pass
    except RequestError0:
        driver.refresh_frame()
    except MaxCardLimitException:
        utilities.sell_cards(driver)
    except JavascriptException:
        driver.switch_to.parent_frame()
        WebDriverWait(driver, 10).until(
                ec.frame_to_be_available_and_switch_to_it(
                    (By.ID, "game_frame")))

