import time

from selenium.common.exceptions import (
    StaleElementReferenceException,
    NoSuchElementException,
    ElementClickInterceptedException,
    ElementNotInteractableException,
    UnexpectedAlertPresentException,
    TimeoutException, JavascriptException)
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import utilities
import web_driver


def initialize_module(driver):

    if driver.switch_to.parent_frame():
        print("switched to parent frame\r")
    if WebDriverWait(driver, 10).until(
            ec.frame_to_be_available_and_switch_to_it((By.ID, "game_frame"))):
        print("switched to game frame\r")


def pick_fight(driver):
    opponent_frames_list = WebDriverWait(driver, 10).until(
        ec.visibility_of_element_located((By.ID, "productList")))

    opponent_frames_list = driver.execute_script(
        "return document.querySelector('#productList');")

    opponent_frame = opponent_frames_list.find_elements_by_tag_name('a')[1]
    driver.execute_script("arguments[0].click();", opponent_frame)

    try:
        WebDriverWait(driver, 10).until(ec.staleness_of(opponent_frames_list))

        weak_attack(driver)
        skip_animation(driver)
        get_battle_results(driver)
    except TimeoutException:
        web_driver.print_temp("timed out :(")

    finally:
        import nav
        nav.arena(driver)


def weak_attack(driver):
    bp = 6 - driver.execute_script("return bpNumTillMax;")

    if bp < 1:
        weak_attack_btn = driver.execute_script(
            "return document.querySelector('#quest_attack_1');")
        driver.execute_script("arguments[0].click();", weak_attack_btn)

        WebDriverWait(driver, 3).until(
            ec.visibility_of_element_located((By.ID, "modal-win-inner")))
        utilities.do_bp(driver, is_event=True)

    weak_attack_btn = driver.execute_script(
        "return document.querySelector('#quest_attack_1');")
    driver.execute_script("arguments[0].click();", weak_attack_btn)


def skip_animation(driver):
    while driver.page() == "/arena/user_confirm":
        time.sleep(1)
        ActionChains(driver).move_to_element_with_offset(
            driver.find_element_by_id("gadget_contents"), 254, 50).click().perform()
        time.sleep(1)
        ActionChains(driver).move_to_element_with_offset(
            driver.find_element_by_id("gadget_contents"), 700, 650).click().perform()


def get_battle_results(driver):
    points_frame = driver.execute_script(
        "return document.querySelector('#scroll_content2');")
    divs = points_frame.find_elements_by_tag_name('div')

    for div in divs:
        driver.execute_script("arguments[0].scrollTop=arguments[1].offsetTop",
                              points_frame, div)
        line = div.text

        if line.startswith("Total Arena pts "):
            pts = int((line.split()[3])[:-2])
            total = int(driver.get_arena_event_points())
            driver.set_arena_event_points(total + pts)

            count = int(driver.get_arena_event_fight_count())
            driver.set_arena_event_fight_count(count + 1)

            if pts < 1000:
                loss = driver.get_arena_event_loss_count()
                driver.set_arena_event_loss_count(loss + 1)

            average = ((total+pts)/(count+1))

            web_driver.print_temp(f"arena_pts: {pts}", temp=False)
            web_driver.print_temp(f"arena_pts_total: {driver.get_arena_event_points()}", temp=False)
            web_driver.print_temp(f"arena_fight_count: {driver.get_arena_event_fight_count()}", temp=False)
            web_driver.print_temp(f"arena_loss_count: {driver.get_arena_event_loss_count()}", temp=False)
            web_driver.print_temp(f"pts/fight: {int(average)}\n\n", temp=False)
            break
