import time

from selenium.common.exceptions import (JavascriptException,
                                        TimeoutException,
                                        StaleElementReferenceException,
                                        NoSuchElementException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import utilities
from custom_exceptions import (MaxCardLimitException,
                               ShopBreakException)


def boss_alert(driver):
    if driver.bot.page() == '/mypage/index':
        try:
            WebDriverWait(driver, 3).until(
                ec.element_to_be_clickable((By.ID, 'boss_alerts_1')))
            alert = driver.find_element(By.ID, 'boss_alerts_1')
            return alert is not None
        except (JavascriptException, TimeoutException):
            return False


def main_page(driver, force_refresh=False):
    try:
        if driver.bot.page() == '/item/item_shop':
            raise ShopBreakException
        elif driver.bot.page() != '/mypage/index' or force_refresh:
            driver.bot.click('id', 'mypage')
    except JavascriptException:
        raise JavascriptException


def slayer_event_page(driver):
    if driver.bot.page() == '/mypage/index':
        hunt = driver.execute_script(
            "return document.querySelector('a[href*=hunt_event_top]');")
        driver.execute_script("arguments[0].click();", hunt)

        WebDriverWait(driver, 5).until(ec.presence_of_all_elements_located(
            (By.CLASS_NAME, 'hexagon_button')))


# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
# Only for Slayer Events
def battle_to_event_stage(driver):
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located(
        (By.ID, 'hunt_result')))

    total_points = driver.execute_script("return app.tower.data.extra_pt")

    if total_points is not None:
        total_points = int(total_points)
        print(f"total event points: {total_points:,}\n")

    result = driver.find_element(By.ID, 'hunt_result')
    close = result.find_element(By.CLASS_NAME, 'closePopup')
    driver.execute_script("arguments[0].click();", close)

    WebDriverWait(driver, 5).until(ec.presence_of_all_elements_located(
        (By.TAG_NAME, 'a')))

    hunt = driver.execute_script(
        "return document.querySelector('a[href*=hunt_start]');")

    driver.execute_script("arguments[0].click();", hunt)
    WebDriverWait(driver, 5).until(ec.staleness_of(hunt))


def battle_page(driver, slayer_event=False):

    if slayer_event or raid_boss_list(driver):

        try:
            WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located((By.CLASS_NAME, 'friend_frame')))

            friend_frames = driver.find_elements(By.CLASS_NAME, "friend_frame")
            ranking_frames = driver.find_elements(By.CLASS_NAME, "ranking_frame")
            container = driver.find_element(By.ID, "scroll_content")
            # for frame in friend_frames:
            for frame in friend_frames:
                driver.execute_script("arguments[0].scrollTop=arguments[1].offsetTop", container, frame)
                info = frame.text.split('\n')
                if driver.account.get('username') in info[-2]:
                    driver.execute_script("arguments[0].click();", frame)
                    WebDriverWait(driver, 3).until(ec.staleness_of(frame))
                    return driver.bot.page() == '/raid/boss_arrival'
        except (IndexError, TimeoutException):
            pass
        return False
    else:
        return False


def quest_to_boss_list(driver, slayer_event=False):
    if slayer_event or driver.bot.page() == '/quest/quest_start':
        cvs = driver.find_element(By.ID, 'canvas')

        ActionChains(driver).move_to_element_with_offset(
            driver.find_element(By.ID, 'gadget_contents'), -275, -100).click().perform()
        WebDriverWait(driver, 3).until(ec.staleness_of(cvs))


def raid_boss_list(driver):
    if driver.bot.page() == '/raid/raid_index':
        return True
    elif driver.bot.page() == '/card/card_max':
        raise MaxCardLimitException

    try:
        main_page(driver)
        driver.bot.click('id', 'boss_alerts_1')
    except NoSuchElementException:

        return False

    return driver.bot.page() == '/raid/raid_index'


def quest(driver):
    try:
        driver.bot.click('class', 'top_menu_1')

        if driver.bot.page() == '/card/card_max':
            raise MaxCardLimitException

        WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.ID,'chapter1')))
        chapter1 = driver.find_element(By.ID, "chapter1")
        driver.execute_script("arguments[0].click()", chapter1)

        WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.ID, 'stage1-link')))
        stage1 = driver.find_element(By.ID, 'stage1-link')
        driver.execute_script("arguments[0].click()", stage1)

        WebDriverWait(driver, 3).until(ec.visibility_of_element_located((By.ID, 'canvas')))

    except NoSuchElementException:
        if driver.find_element(By.ID, 'gadget_contents').text == "Request Error(0)":
            driver.bot.refresh_frame()
    except MaxCardLimitException:
        raise MaxCardLimitException


# noinspection PyBroadException
def event_page(driver, event="hunt"):
    if "tower" in event:
        ref = driver.bot.find_href('tower_event_top')
    else:
        ref = driver.bot.find_href('hunt_event_top')

    driver.execute_script("arguments[0].click();", ref)
    WebDriverWait(driver, 10).until(ec.staleness_of(ref))
    return True


def event_stage(driver):
    ref = driver.bot.find_href('hunt_start')
    driver.execute_script("arguments[0].click();", ref)
    WebDriverWait(driver, 10).until(ec.staleness_of(ref))


def gifts(driver):
    driver.bot.click('class', 'button-present')
    if driver.bot.page() == '/card/card_max':
        raise MaxCardLimitException
    else:
        return driver.bot.page() == '/present/index'


def unclaimed_gifts(driver):
    main_page(driver)

    try:
        WebDriverWait(driver, 3).until(ec.visibility_of_element_located(
            (By.CLASS_NAME, 'button-present')))
        gifts_button = driver.find_element(By.CLASS_NAME, 'button-present')
        icon_url = gifts_button.get_attribute('style').split('"')[1]
        return 'present_2' in icon_url
    except NoSuchElementException:
        print("no such gift button exception", flush=True)
    except AttributeError:
        utilities.my_traceback()
    except StaleElementReferenceException:
        utilities.my_traceback()
    except TimeoutException:
        if driver.find_element(By.ID, 'gadget_contents').text == 'Request Error(0)':
            driver.bot.refresh_frame()


def boss_recon(driver):
    status = WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located(
        (By.CLASS_NAME, 'quest_boss_status_1')))
    name = status[0].text
    if "(AR)" in name:
        utilities.print_temp("fighting AR", False)

    if driver.bot.boss_name is None:
        driver.bot.boss_name = name
        import output
        output.boss_counter(driver)


def defeat_retry(driver):
    buttons = WebDriverWait(driver, 5).until(
        ec.presence_of_all_elements_located(
            (By.CLASS_NAME, 'decision_button_column_1')))

    for b in buttons:
        if "Retry" in b.text:
            driver.execute_script("arguments[0].click();", b)
            WebDriverWait(driver, 5).until(ec.staleness_of(b))
            break


def arena(driver):
    if driver.bot.page() != "/arena/battle_index":
        d = driver.execute_script("return document.querySelector('.top_menu_2');")
        driver.execute_script("arguments[0].click();", d)


def return_to_event(driver):
    goto_event = driver.execute_script(
        "return document.querySelector('#main_frame > a:nth-child(7)');")
    driver.execute_script("arguments[0].click();", goto_event)
    time.sleep(1)
    goto_event = driver.execute_script(
        "return document.querySelector('#stage_choice');")
    driver.execute_script("arguments[0].click();", goto_event)
    time.sleep(1)
    goto_event = driver.execute_script(
        "return document.querySelector('#event_menu_2 > div:nth-child(3) > a');")
    driver.execute_script("arguments[0].click();", goto_event)