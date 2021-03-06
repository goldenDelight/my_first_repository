import time

from selenium.common.exceptions import (
    TimeoutException,
    JavascriptException, NoSuchElementException, WebDriverException,
    MoveTargetOutOfBoundsException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import battle
import nav
import utilities
import web_driver


def fight(driver, slayer_event=False):
    """
    :param driver:
    :param slayer_event:
    """
    import startup

    battle.start_battle(driver)
    battle.get_partner(driver)

    bp = 6 - driver.execute_script("return bpNumTillMax;")
    try:
        name = WebDriverWait(driver, 3).until(ec.visibility_of_element_located((By.CLASS_NAME, "quest_boss_status_1")))
        if "(AR)" in name.text:
            if bp < 3:
                battle.full_attack(driver)
                WebDriverWait(driver, 3).until(ec.visibility_of_element_located((By.ID, "modal-win-inner")))
                utilities.do_bp(driver, slayer_event)
                battle.full_attack(driver)
            else:
                battle.full_attack(driver)

            web_driver.print_temp("fully attacking", False)

        elif bp < 1:
        # if bp < 1:
            battle.weak_attack(driver)
            WebDriverWait(driver, 3).until(ec.visibility_of_element_located((By.ID, "modal-win-inner")))
            utilities.do_bp(driver, slayer_event)
            battle.weak_attack(driver)
        else:
            battle.weak_attack(driver)

        web_driver.print_temp("weakly attacking", False)

    except NoSuchElementException:
        pass
    except TimeoutException:
        try:
            driver.find("css", "a.closePopup:nth-child(6) > div:nth-child(1)").click()
        except AttributeError:
            return
    except (WebDriverException, JavascriptException, AttributeError):
        web_driver.tb()

    finally:
        if slayer_event:
            skip_animation(driver)
            if driver.page() == "/raid/boss_fail/":
                nav.defeat_retry(driver)
                fight(driver, slayer_event)
        else:
            driver.wait_for("id", "canvas_box")
            driver.wait_for("id", "canvas")
            driver.execute_script("gadgets.util.runOnLoadHandlers();")
            startup.game_start(driver)


def skip_animation(driver):
    """
    Skips do_battle cinematic. Loop of action-chain clicks at hardcoded coordinates of 'skip'
    button hidden under canvas. The loop breaks if canvas returns as None, or after 3s.
    """

    for i in range(35):
        try:
            ActionChains(driver).move_to_element_with_offset(
                driver.find_element_by_id("gadget_contents"), 254, 50).click().perform()

            time.sleep(0.1)

            if driver.find_element_by_id("hunt_result"):
                break

        except NoSuchElementException:
            pass
        except (TimeoutException, AttributeError, MoveTargetOutOfBoundsException):
            web_driver.tb()
            web_driver.print_temp("skip animation: Timeout")
            break

    web_driver.print_temp("skip animation: success")
