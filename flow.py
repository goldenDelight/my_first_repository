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


def slayer_event(driver):
    refocus_frame(driver)

    if driver.page() == '/raid/boss_achievement':
        try:
            canvas = driver.execute_script(
                "return document.querySelector('#canvas');")
            canvas.click()
        except AttributeError:
            pass
    try:

        if driver.page() == '/item/item_shop':
            raise ShopBreakException

        if driver.page() == '/raid/boss_arrival':
            logic.fight(driver, slayer_event=True)
            nav.battle_to_event_stage(driver)

        elif driver.page() == '/hunt/hunt_start':
            quest.grind(driver, slayer_event=True)
            nav.quest_to_boss_list(driver, slayer_event=True)
            nav.battle_page(driver, slayer_event=True)
            logic.fight(driver, slayer_event=True)
            nav.battle_to_event_stage(driver)

        elif driver.page() == '/hunt/raid_list':
            if nav.battle_page(driver, slayer_event=True):
                logic.fight(driver, slayer_event=True)
                nav.battle_to_event_stage(driver)

        elif driver.page() == '/hunt/hunt_event_top':
            if check_slayer_boss(driver):
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

        elif driver.page() == '/mypage/index':
            nav.event_page(driver)

        elif driver.page() == '/card/card_max':
            utilities.sell_cards(driver)
            nav.event_page(driver)
            check_slayer_boss(driver)
            nav.event_stage(driver)

        elif driver.page() == '/raid/boss_help_select':
            import battle
            battle.get_partner(driver)

    except TimeoutException:
        pass
    except JavascriptException:
        refocus_frame(driver)


def check_slayer_boss(driver):
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, 'a')))
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
    import gifts
    import nav
    import quest

    try:
        if driver.page() == '/item/item_shop':
            raise ShopBreakException

        if nav.unclaimed_gifts(driver):
            nav.gifts(driver)
            gifts.get_gifts(driver)

        if nav.battle_page(driver):
            nav.boss_recon(driver)
            decision_tree(driver)

        else:
            nav.quest(driver)
            quest.grind(driver)
            nav.quest_to_boss_list(driver)
            nav.battle_page(driver)
            nav.boss_recon(driver)
            decision_tree(driver)

    except TimeoutException:
        pass
    except RequestError0:
        driver.refresh_frame()
    except MaxCardLimitException:
        utilities.sell_cards(driver)
    except JavascriptException:
        refocus_frame(driver)


# decides: fight now, stall for assist, or stall for bp
def decision_tree(driver):
    """
    :param driver: :return N/A: Called when driver reaches boss battle page,
    determines course of action based on boss and current BP/cooldown:

    request assist - if boss is not oni or speed, clicks 'request assist',
    stalls for assist on main page. wait for cooldown - if boss is oni or
    speed but BP cooldown is < 10min, stalls for cooldown on main page fight
    - when BP capped at 6 - BP > 0, boss is oni or speed and cooldown >10min
    - BP is 0, boss is oni, BP cooldown >10min (uses 1 bp pot)
    """

    import status
    bp = status.current_bp(driver)

    if driver.boss_name is None:
        WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located(
            (By.CLASS_NAME, 'quest_boss_status_1')))
        status = driver.find_elements_by_class_name('quest_boss_status_1')
        name = status[0].text
        if name is not None:
            driver.boss_name = name
            output.boss_counter(driver)

    web_driver.print_temp("the council will decide your fate")

    if bp == 6:
        print("6 bp == fight")
        logic.fight(driver)

    elif "Red Oni" in driver.boss_name:
        web_driver.print_temp(f"red oni in boss name is True")
        nav.boss_alert(driver)
        nav.raid_boss_list(driver)
        nav.battle_page(driver)
        logic.fight(driver)

    elif "Speed Demon" in driver.boss_name:
        web_driver.print_temp(f"speed demon in boss name is True")

        if driver.initial_bp_cooldown <= 10:
            web_driver.print_temp(f"bp cooldown <= 10 min")
            time.sleep(60 * driver.initial_bp_cooldown)
            stall(driver, False)
        else:
            web_driver.print_temp(f"bp cooldown not <= 10 min")
        nav.boss_alert(driver)
        nav.raid_boss_list(driver)
        nav.battle_page(driver)
        logic.fight(driver)

    else:  # request assist
        web_driver.print_temp("request assist")
        try:
            driver.click('class', 'raid_help_button')
        except NoSuchElementException:
            pass

        web_driver.print_temp("stall for assist")
        stall(driver, bp)


# boss_recon for boss_name in 10s loop
# forces fight after 40min or if initial_bp maxes out
def stall(driver, full_restore=True):
    import status
    import nav

    if driver.initial_bp >= 5 or full_restore:
        target_bp = 6
    else:
        target_bp = driver.initial_bp + 1

    print(f"starting bp = {status.current_bp(driver)}\n"
          f"target bp = {target_bp}")
    web_driver.print_temp("starting stall", temp=False)

    try:
        while True:
            nav.main_page(driver, force_refresh=True)
            if status.current_bp(driver) >= target_bp:
                break
            elif nav.unclaimed_gifts(driver):
                web_driver.print_temp("got assisted", temp=False)
                break
            else:
                web_driver.animated_text("stalling")
                time.sleep(15)
    except TypeError:
        raise RequestError0

    driver.done_stalling = status.current_bp(driver) == target_bp


def refocus_frame(driver):
    driver.switch_to.parent_frame()
    WebDriverWait(driver, 10).until(
        ec.frame_to_be_available_and_switch_to_it((By.ID, 'game_frame')))
