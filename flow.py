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
import taba_bot
from handlers import MaxCardLimitException, RequestError0, ShopBreakException


def slayer_event(driver):
    driver.bot.refocus_frame()

    if driver.bot.page() == '/raid/boss_achievement':
        try:
            canvas = driver.execute_script(
                "return document.querySelector('#canvas');")
            driver.bot.click()
        except AttributeError:
            pass
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

        elif driver.bot.page() == '/mypage/index':
            nav.event_page(driver)

        elif driver.bot.page() == '/card/card_max':
            utilities.sell_cards(driver)
            nav.event_page(driver)
            check_slayer_boss(driver)
            nav.event_stage(driver)

        elif driver.bot.page() == '/raid/boss_help_select':
            import battle
            battle.get_partner(driver)

    except TimeoutException:
        pass
    except JavascriptException:
        driver.bot.refocus_frame()


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
        if driver.bot.page() == '/item/item_shop':
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
        driver.bot.refresh_frame()
    except MaxCardLimitException:
        utilities.sell_cards(driver)
    except JavascriptException:
        driver.bot.refocus_frame()


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

    bp = driver.bot.check_current_bp()

    if driver.bot.boss_name is None:
        WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located(
            (By.CLASS_NAME, 'quest_boss_status_1')))
        status = driver.find_elements_by_class_name('quest_boss_status_1')
        name = status[0].text
        if name is not None:
            driver.bot.boss_name = name
            output.boss_counter(driver.bot)

    taba_bot.print_temp("the council will decide your fate")

    if bp == 6:
        print("6 bp == fight")
        logic.fight(driver)

    elif "Red Oni" in driver.bot.boss_name:
        taba_bot.print_temp(f"red oni in boss name is True")
        nav.boss_alert(driver)
        nav.raid_boss_list(driver)
        nav.battle_page(driver)
        logic.fight(driver)

    elif "Speed Demon" in driver.bot.boss_name:
        taba_bot.print_temp(f"speed demon in boss name is True")

        if driver.bot.initial_bp_cooldown <= 10:
            taba_bot.print_temp(f"bp cooldown <= 10 min")
            time.sleep(60 * driver.bot.initial_bp_cooldown)
            stall(driver, False)
        else:
            taba_bot.print_temp(f"bp cooldown not <= 10 min")
        nav.boss_alert(driver)
        nav.raid_boss_list(driver)
        nav.battle_page(driver)
        logic.fight(driver)

    else:  # request assist
        taba_bot.print_temp("request assist")
        try:
            driver.bot.click('class', 'raid_help_button')
        except NoSuchElementException:
            pass

        taba_bot.print_temp("stall for assist")
        stall(driver, bp)


# boss_recon for boss_name in 10s loop
# forces fight after 40min or if initial_bp maxes out
def stall(driver, full_restore=True):
    import nav

    if driver.bot.initial_bp >= 5 or full_restore:
        target_bp = 6
    else:
        target_bp = driver.bot.initial_bp + 1

    print(f"starting bp = {driver.bot.check_current_bp()}\n"
          f"target bp = {target_bp}")
    taba_bot.print_temp("starting stall", temp=False)

    try:
        while True:
            nav.main_page(driver, force_refresh=True)
            if driver.bot.check_current_bp() >= target_bp:
                break
            elif nav.unclaimed_gifts(driver):
                taba_bot.print_temp("got assisted", temp=False)
                break
            else:
                taba_bot.animated_text("stalling")
    except TypeError:
        raise RequestError0

    driver.done_stalling = driver.bot.check_current_bp() == target_bp
