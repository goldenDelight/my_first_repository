import selenium.webdriver.support.expected_conditions as ec
from selenium.common.exceptions import (JavascriptException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import logic
import nav
import stage
import utilities

from custom_exceptions import \
    MaxCardLimitException, \
    RequestError0, \
    ShopBreakException

vanquish_points_goal = 200000000
full_attack_AR = False
current_points = 0


def nav_to_event_splash(driver):
    if 'hunt_event_top' not in driver.bot.page():
        ref = driver.bot.find_href('hunt_event_top')
        driver.execute_script("arguments[0].click();", ref)


def nav_to_boss_list(driver):
    if 'raid_list' not in driver.bot.page():
        ref = driver.bot.find_href('raid_list')
        driver.execute_script("arguments[0].click();", ref)


def nav_to_boss(driver):
    if 'boss_arrival' not in driver.bot.page():
        ref = driver.bot.find_href('boss_arrival')
        driver.execute_script("arguments[0].click();", ref)


def nav_to_stage(driver):
    if 'hunt_start' not in driver.bot.page():
        ref = driver.bot.find_href('hunt_start')
        driver.execute_script("arguments[0].click();", ref)


# TODO: change click method to javascript click to avoid 'click intercepted'
#  exceptions when a popup is displayed

def run_event():
    global current_points
    global vanquish_points_goal

    # return current_points < vanquish_points_goal
    return True


def grind(driver):
    driver.bot.refocus_frame()

    if 'boss_achievement' in driver.bot.page():
        try:
            canvas = driver.execute_script(
                "return document.querySelector('#canvas');")
            canvas.click()
        except AttributeError:
            try:
                href = driver.bot.find_href('hunt_start')
                driver.execute_script("arguments[0].click();", href)
            except AttributeError:
                nav.main_page(driver)
    try:

        if 'item_shop' in driver.bot.page():
            raise ShopBreakException

        if 'boss_arrival' in driver.bot.page():
            logic.fight(driver,
                        slayer_event=True,
                        full_attack_AR=full_attack_AR)
            nav.battle_to_event_stage(driver)

        elif 'hunt_start' in driver.bot.page():
            stage.grind(driver, slayer_event=True)
            nav.quest_to_boss_list(driver, slayer_event=True)
            nav.battle_page(driver, slayer_event=True)
            logic.fight(driver,
                        slayer_event=True,
                        full_attack_AR=full_attack_AR)
            nav.battle_to_event_stage(driver)

        elif 'list' in driver.bot.page():
            if nav.battle_page(driver, slayer_event=True):
                logic.fight(driver,
                            slayer_event=True,
                            full_attack_AR=full_attack_AR)
                nav.battle_to_event_stage(driver)

        elif 'hunt_event_top' in driver.bot.page():
            if check_for_boss(driver):
                if nav.battle_page(driver, slayer_event=True):
                    logic.fight(driver,
                                slayer_event=True,
                                full_attack_AR=full_attack_AR)
                    nav.battle_to_event_stage(driver)
                else:
                    nav.event_stage(driver)
                    stage.grind(driver, slayer_event=True)
                    nav.quest_to_boss_list(driver, slayer_event=True)
                    nav.battle_page(driver, slayer_event=True)
                    logic.fight(driver,
                                slayer_event=True,
                                full_attack_AR=full_attack_AR)
                    nav.battle_to_event_stage(driver)

            else:
                nav.event_stage(driver)
                stage.grind(driver, slayer_event=True)
                nav.quest_to_boss_list(driver, slayer_event=True)
                nav.battle_page(driver)
                logic.fight(driver,
                            slayer_event=True,
                            full_attack_AR=full_attack_AR)
                nav.battle_to_event_stage(driver)

        elif 'index' in driver.bot.page():
            nav.event_page(driver)

        elif 'card_max' in driver.bot.page():
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


def battle_to_event_stage(driver):
    global vanquish_points_goal
    global current_points

    WebDriverWait(driver, 5).until(ec.visibility_of_element_located(
        (By.ID, 'hunt_result')))

    current_points = int(driver.execute_script("return app.tower.data.extra_pt"))

    if current_points is not None:
        print(f"total event points: {current_points:,}\n")

        if current_points > vanquish_points_goal:
            raise ShopBreakException

    result = driver.find_element(By.ID, 'hunt_result')
    close = result.find_element(By.CLASS_NAME, 'closePopup')
    driver.execute_script("arguments[0].click();", close)

    WebDriverWait(driver, 5).until(ec.presence_of_all_elements_located(
        (By.TAG_NAME, 'a')))

    hunt = driver.execute_script(
        "return document.querySelector('a[href*=hunt_start]');")

    driver.execute_script("arguments[0].click();", hunt)
    WebDriverWait(driver, 5).until(ec.staleness_of(hunt))


def event_stage(driver):
    ref = driver.bot.find_href('hunt_start')
    driver.execute_script("arguments[0].click();", ref)
    WebDriverWait(driver, 10).until(ec.staleness_of(ref))


def event_page(driver):
    ref = driver.bot.find_href('hunt_event_top')
    driver.execute_script("arguments[0].click();", ref)
    WebDriverWait(driver, 10).until(ec.staleness_of(ref))
    return True
