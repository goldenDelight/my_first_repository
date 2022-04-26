import selenium.webdriver.support.expected_conditions as ec
from selenium.common.exceptions import (JavascriptException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import logic
import nav
import stage
import utilities

from custom_exceptions import \
    MaxCardLimitException, \
    RequestError0, \
    ShopBreakException


def nav_to_event_splash(driver):
    if '/hunt/hunt_event_top' not in driver.bot.page():
        links = driver.execute_script("return document.querySelectorAll('a');")
        for link in links:
            if 'hunt_event_top' in link.get_attribute('href'):
                driver.execute_script("arguments[0].click();", link)
                break


def nav_to_boss_list(driver):
    if '/hunt/raid_list' not in driver.bot.page():
        links = driver.execute_script("return document.querySelectorAll('a');")
        for link in links:
            if '/hunt/raid_list' in link.get_attribute('href'):
                driver.execute_script("arguments[0].click();", link)
                break


def nav_to_boss(driver):
    if '/raid/boss_arrival' not in driver.bot.page():
        links = driver.execute_script("return document.querySelectorAll('a');")
        for link in links:
            if '/raid/boss_arrival' in link.get_attribute("href"):
                driver.execute_script("arguments[0].click();", link)
                break


def nav_to_stage(driver):
    if '/hunt/hunt_start' not in driver.bot.page():
        links = driver.execute_script("return document.querySelectorAll('a');")
        for link in links:
            if '/hunt/hunt_start' in link.get_attribute('href'):
                driver.execute_script("arguments[0].click();", link)
                break


def grind(driver):
    driver.bot.refocus_frame()

    if driver.bot.page() == '/raid/boss_achievement':
        try:
            canvas = driver.execute_script(
                "return document.querySelector('#canvas');")
            canvas.click()
        except AttributeError:
            try:
                href = driver.bot.find_href('hunt_start')
                href.click()
            except AttributeError:
                nav.main_page(driver)
    try:

        if driver.bot.page() == '/item/item_shop':
            raise ShopBreakException

        if driver.bot.page() == '/raid/boss_arrival':
            logic.fight(driver, slayer_event=True)
            nav.battle_to_event_stage(driver)

        elif driver.bot.page() == '/hunt/hunt_start':
            quest.grind(driver, slayer_event=True)
            nav.quest_to_boss_list(driver, slayer_event=True)
            nav.battle_page(driver, slayer_event=True)
            logic.fight(driver, slayer_event=True)
            nav.battle_to_event_stage(driver)

        elif driver.bot.page() == '/hunt/raid_list':
            if nav.battle_page(driver, slayer_event=True):
                logic.fight(driver, slayer_event=True)
                nav.battle_to_event_stage(driver)

        elif driver.bot.page() == '/hunt/hunt_event_top':
            if check_for_boss(driver):
                if nav.battle_page(driver, slayer_event=True):
                    logic.fight(driver, slayer_event=True)
                    nav.battle_to_event_stage(driver)
                else:
                    nav.event_stage(driver)
                    stage.grind(driver, slayer_event=True)
                    nav.quest_to_boss_list(driver, slayer_event=True)
                    nav.battle_page(driver, slayer_event=True)
                    logic.fight(driver, slayer_event=True)
                    nav.battle_to_event_stage(driver)

            else:
                nav.event_stage(driver)
                stage.grind(driver, slayer_event=True)
                nav.quest_to_boss_list(driver, slayer_event=True)
                nav.battle_page(driver)
                logic.fight(driver, slayer_event=True)
                nav.battle_to_event_stage(driver)

        elif driver.bot.page() == '/mypage/index':
            nav.event_page(driver)

        elif driver.bot.page() == '/card/card_max':
            utilities.sell_cards(driver)
            nav.event_page(driver)
            check_for_boss(driver)
            nav.event_stage(driver)

        elif driver.bot.page() == '/raid/boss_help_select':
            import battle
            battle.get_partner(driver)

    except TimeoutException:
        pass
    except JavascriptException:
        driver.bot.refocus_frame()


def check_for_boss(driver):
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, 'a')))
        boss_list = driver.execute_script(
            "return document.querySelector('a[href*=raid_list]');")
        driver.execute_script("arguments[0].click();", boss_list)
        return True
    except (TimeoutException,
            AttributeError,
            JavascriptException):
        return False


def grind_routine(driver):
    import nav
    import quest

    try:
        if driver.bot.page() == '/item/item_shop':
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
        driver.bot.refresh_frame()
    except MaxCardLimitException:
        utilities.sell_cards(driver)
    except JavascriptException:
        driver.switch_to.parent_frame()
        WebDriverWait(driver, 10).until(
                ec.frame_to_be_available_and_switch_to_it(
                    (By.ID, 'game_frame')))
