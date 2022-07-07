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
import startup
import utilities
from custom_exceptions import (MaxCardLimitException,
                               ShopBreakException)


def grind(driver):
    import gifts
    import nav
    import stage

    try:
        if driver.bot.page() == '/item/item_shop':
            raise ShopBreakException

        elif driver.execute_script("return document.querySelector('#information');") is not None:
            startup.game_start(driver)

        if nav.unclaimed_gifts(driver):
            nav.gifts(driver)
            gifts.get_gifts(driver)
            return

        if nav.battle_page(driver):
            nav.boss_recon(driver)
            decision_tree(driver)

        else:
            nav.quest(driver)
            stage.grind(driver)
            nav.quest_to_boss_list(driver)
            nav.battle_page(driver)
            nav.boss_recon(driver)
            decision_tree(driver)

    except TimeoutException:
        pass
    except MaxCardLimitException:
        utilities.sell_cards(driver)
    except JavascriptException:
        driver.bot.refocus_frame()


# decides: fight now, stall for assist, or stall for my_bp
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
        status = driver.find_elements(By.CLASS_NAME, 'quest_boss_status_1')

        if name := status[0].text:
            driver.bot.boss_name = name
            output.boss_counter(driver.bot)

    print("the council will decide your fate")

    if bp == 6:
        print("6 bp == fight")
        logic.fight(driver)

    elif "Red Oni" in driver.bot.boss_name:
        utilities.print_temp(f"red oni in boss name is True")
        nav.boss_alert(driver)
        nav.raid_boss_list(driver)
        nav.battle_page(driver)
        logic.fight(driver)

    elif "Speed Demon" in driver.bot.boss_name:
        if bp_cd := driver.bot.bp_cooldown() <= 10:
            utilities.print_temp(f"bp cooldown <= 10 min")
            time.sleep(60 * bp_cd)
            stall(driver, False)
        else:
            utilities.print_temp(f"bp cooldown not <= 10 min")
        nav.boss_alert(driver)
        nav.raid_boss_list(driver)
        nav.battle_page(driver)
        logic.fight(driver)

    else:  # request assist
        utilities.print_temp("request assist")
        try:
            driver.bot.click('class', 'raid_help_button')
        except NoSuchElementException:
            pass

        utilities.print_temp("stall for assist")
        stall(driver, bp)


# boss_recon for boss_name in 10s loop
# forces fight after 40min or if initial_bp maxes out
def stall(driver, full_restore=False):
    import nav

    if driver.bot.initial_bp >= 5 or full_restore:
        target_bp = 6
    else:
        target_bp = driver.bot.initial_bp + 1

    print(f"starting bp = {driver.bot.check_current_bp()}\n"
          f"target bp = {target_bp}")
    utilities.print_temp("starting stall", temp=False)

    try:
        while True:
            nav.main_page(driver, force_refresh=True)
            if driver.bot.check_current_bp() >= target_bp:
                break
            elif nav.unclaimed_gifts(driver):
                utilities.print_temp("got assisted", temp=False)
                break
            else:
                utilities.animated_text("stalling")
    except TypeError:
        driver.bot.refresh_frame()

    driver.done_stalling = (driver.bot.check_current_bp() == target_bp)
