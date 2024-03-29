from selenium.common.exceptions import (
    TimeoutException,
    JavascriptException,
    NoSuchElementException,
    WebDriverException,
    MoveTargetOutOfBoundsException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import battle_log
import battle
import nav
import utilities


def fight(driver, slayer_event=False, full_attack_AR=False):
    """
    :param full_attack_AR:
    :param driver:
    :param slayer_event:
    """
    import startup

    battle.start_battle(driver)
    battle.get_partner(driver)

    bp = 6 - driver.execute_script("return bpNumTillMax;")
    try:
        name = WebDriverWait(driver, 3).until(
            ec.visibility_of_element_located((
                By.CLASS_NAME, 'quest_boss_status_1')))

        if (full_attack_AR and "(AR)") or "(Hell)" in name.text:
            if bp < 3:
                battle.full_attack(driver)
                WebDriverWait(driver, 3).until(
                    ec.visibility_of_element_located((
                        By.ID, 'modal-win-inner')))

                utilities.do_bp(driver, slayer_event)

            battle.full_attack(driver)
            utilities.print_temp("fully attacking", False)

        elif bp < 1:
            battle.weak_attack(driver)
            WebDriverWait(driver, 3).until(
                ec.visibility_of_element_located((
                    By.ID, 'modal-win-inner')))

            utilities.do_bp(driver, slayer_event)
            battle.weak_attack(driver)

        else:
            battle.weak_attack(driver)

    except NoSuchElementException:
        pass
    except TimeoutException:
        try:
            css = "a.closePopup:nth-child(6) > div:nth-child(1)"
            element = WebDriverWait(driver, 5).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, css)))

            element.click()
        except TimeoutException:
            return

    except (WebDriverException,
            JavascriptException,
            AttributeError):
        utilities.my_traceback()

    finally:
        if slayer_event:
            skip_animation(driver, battle_page="/raid/boss_bp")
            # battle_log.track_slayer_battle(driver)

            if driver.bot.page() == '/raid/boss_fail/':
                nav.defeat_retry(driver)
                fight(driver, slayer_event)
        else:
            try:
                WebDriverWait(driver, 3).until(
                    ec.element_to_be_clickable((By.ID, 'canvas_box')))

            except TimeoutException:
                WebDriverWait(driver, 3).until(
                    ec.element_to_be_clickable((By.ID, 'canvas')))

            driver.execute_script("gadgets.util.runOnLoadHandlers();")
            startup.game_start(driver)


def skip_animation(driver, battle_page):
    """
    Skips do_battle cinematic. Loop of action-chain clicks at hardcoded
    coordinates of 'skip' button hidden under canvas. The loop breaks if
    canvas returns as None, or after 3s.
    """

    while driver.bot.page() == battle_page:
        try:
            driver.bot.refocus_frame()
            gc = driver.find_element(By.ID, 'gadget_contents')
            ActionChains(driver) \
                .move_to_element(gc) \
                .move_by_offset(-250, -290) \
                .click() \
                .perform()
        except NoSuchElementException:
            pass
        except (TimeoutException,
                AttributeError,
                MoveTargetOutOfBoundsException):
            utilities.my_traceback()
            break
    print("\n")
    # taba_bot.print_temp("skip animation: success")
