from selenium.common.exceptions import (
    TimeoutException,
    WebDriverException,
    JavascriptException,
    NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
import startup
import utilities


def start_battle(driver):
    try:
        battle_btn = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located(
                (By.CSS_SELECTOR, '#battle_start_button')))
        driver.execute_script("arguments[0].click();", battle_btn)
        return True
    except TimeoutException:
        return False


def get_partner(driver):
    try:
        partner_frame = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((
                By.CSS_SELECTOR, '.friend_frame')))

        partner_frame.click()
        return True

    except TimeoutException:

        try:
            partner_frame = driver.execute_script(
                "return document.querySelector('.friend_frame')")
            partner_frame.click()
            return True

        except JavascriptException:
            utilities.my_traceback()
        except AttributeError:
            utilities.my_traceback()
            if driver.find_element(By.ID, 'gadget_contents').text == "Request Error(0)":
                driver.execute_script("gadgets.util.runOnLoadHandlers();")
                startup.game_start(driver)

    return False


def weak_attack(driver):
    utilities.print_temp("weakly attacking")
    attack = WebDriverWait(driver, 5).until(ec.element_to_be_clickable(
        (By.CSS_SELECTOR, '#quest_attack_1')))
    driver.execute_script("arguments[0].click();", attack)


def normal_attack(driver):
    utilities.print_temp("normally attacking")
    attack = WebDriverWait(driver, 5).until(ec.element_to_be_clickable(
        (By.CSS_SELECTOR, '#quest_attack_2')))
    driver.execute_script("arguments[0].click();", attack)


def full_attack(driver):
    utilities.print_temp("fully attacking")
    attack = WebDriverWait(driver, 5).until(ec.element_to_be_clickable(
        (By.CSS_SELECTOR, '#quest_attack_3')))
    driver.execute_script("arguments[0].click();", attack)


def req_assist(driver):
    utilities.print_temp("request assist")

    try:
        driver.bot.click('class', 'raid_help_button')
    except (TimeoutException, AttributeError, WebDriverException):
        pass
    except NoSuchElementException:
        utilities.my_traceback()
        boss_timer = driver.find_element(By.ID, 'raid_time_rimit')
        if boss_timer is not None and boss_timer.is_displayed():
            utilities.print_temp("assist already requested")
        elif driver.find_element(By.ID, 'gadget_contents').text == "Request Error(0)":
            driver.bot.refresh_frame()
