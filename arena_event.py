import time

from selenium.common.exceptions import (
    TimeoutException, JavascriptException, NoSuchElementException)
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import nav
import utilities
import logic

# TODO:
#  reformat summaries
#   use a heading with the time with rest indented
#   opponent name (with total win/loss count)
#   opponent def
#   my mean and median atk
#   actual arena event points
#   average arena points per BP spent
#  avoid opponents I've lost to
#  check for rank-up battle availability
#  check/change decks based on fever/rank-up
from custom_exceptions import ShopBreakException

shit_list = {}
event_points: int = 0
fight_count = 0
loss_count = 0
op_name = None
global pts


def grind(driver):

    if event_points > 2000000:
        raise ShopBreakException

    if driver.bot.page() == '/item/item_shop':
        raise ShopBreakException

    fever = False

    driver.bot.refocus_frame()

    if '/arena/battle_index' not in driver.bot.page():
        nav.arena(driver)

    time.sleep(1)
    print(driver.execute_script(
        "return document.querySelector('#fev_timer');").text)

    if driver.execute_script(
            "return document.querySelector('#fev_timer');").text != "":
        print('fever time yes')
        fever = True

    pick_fight(driver, fever)
    logic.skip_animation(driver, battle_page="/arena/user_confirm")
    get_battle_results(driver)
    nav.arena(driver)


def pick_fight(driver, fever):
    global shit_list
    global op_name

    WebDriverWait(driver, 5).until(
        ec.visibility_of_element_located((By.ID, "productList")))

    for i in range(3):
        driver.bot.refocus_frame()
        products = driver.execute_script(
            "return document.querySelector('#productList');")
        frames = products.find_elements(By.TAG_NAME, 'a')
        opponent = frames[i].text.split()

        if (op_name := opponent[0]) not in shit_list:
            if "Advancement" not in opponent:
                driver.execute_script("arguments[0].click();", frames[i])
                WebDriverWait(driver, 10).until(ec.staleness_of(frames[i]))
                break

    if fever:
        weak_attack(driver)
    else:
        normal_attack(driver)


def weak_attack(driver):
    bp = 6 - driver.execute_script("return bpNumTillMax;")

    if bp < 1:
        weak_attack_btn = driver.execute_script(
            "return document.querySelector('#quest_attack_1');")
        driver.execute_script("arguments[0].click();", weak_attack_btn)

        WebDriverWait(driver, 3).until(
            ec.visibility_of_element_located((By.ID, "modal-win-inner")))
        utilities.do_bp(driver, event_grind=True)

    weak_attack_btn = driver.execute_script(
        "return document.querySelector('#quest_attack_1');")
    driver.execute_script("arguments[0].click();", weak_attack_btn)


def normal_attack(driver):
    bp = 6 - driver.execute_script("return bpNumTillMax;")

    if bp < 2:
        normal_attack_btn = driver.execute_script(
            "return document.querySelector('#quest_attack_2');")
        driver.execute_script("arguments[0].click();", normal_attack_btn)

        WebDriverWait(driver, 3).until(
            ec.visibility_of_element_located((By.ID, "modal-win-inner")))
        utilities.do_bp(driver, event_grind=True)

    try:
        normal_attack_btn = driver.execute_script(
            "return document.querySelector('#quest_attack_2');")
        driver.execute_script("arguments[0].click();", normal_attack_btn)
    except JavascriptException:
        WebDriverWait(driver, 4).until(
            ec.element_to_be_clickable((By.ID, "quest_attack_2"))).click()


def skip_animation(driver):
    while driver.bot.page() == "/arena/user_confirm":
        time.sleep(1)
        ActionChains(driver).move_to_element_with_offset(
            driver.find_element(By.ID, "gadget_contents"), 254,
            50).click().perform()
        time.sleep(1)
        ActionChains(driver).move_to_element_with_offset(
            driver.find_element(By.ID, "gadget_contents"), 700,
            650).click().perform()


def get_battle_results(driver):
    global event_points
    global fight_count
    global loss_count

    driver.bot.refocus_frame()
    op_def = 0
    me_atk = 0
    result = 'win'

    fight_count += 1

    points_frame = driver.execute_script(
        "return document.querySelector('#scroll_content2');")
    divs = points_frame.find_elements(By.TAG_NAME, 'div')

    for div in divs:
        driver.execute_script(
            "arguments[0].scrollTop=arguments[1].offsetTop", points_frame, div)

        line = div.text

        if line.startswith("Total Arena pts "):
            pts = int((line.split()[3])[:-2])
            event_points += pts

            if pts < 1000:
                result = "loss"
                loss_count += 1

        try:
            shadows = driver.execute_script(
                "return document.querySelectorAll('.shadow');")
            me_atk = int(shadows[0].text)
            op_def = int(shadows[1].text)
        except AttributeError:
            pass

    utilities.print_temp(f"Result: {result}\n\tpoints: {pts:,}", temp=False)
    if result == 'loss':
        shit_list[op_name] = op_def
        print(f"\topponent: {op_name} (added to shit list)", flush=True)
    else:
        print(f"\topponent: {op_name}", flush=True)

    print(f"\twin/loss: {fight_count-loss_count}/{loss_count}", flush=True)
    print(f"\tpoints per fight: {int(event_points/fight_count):,}", flush=True)
    print(f"\tmy atk: {me_atk:,}", flush=True)
    print(f"\top def: {op_def:,}", flush=True)

    driver.bot.arena_event_points += pts


def special_deck(driver):
    driver.bot.refocus_frame()
    child = driver.find_element(By.XPATH,
                                '//*[@id="main_frame_battle"]/div[2]/img[5]')
    return 'C00000a' in child.get_attribute('src')


def deck_edit(driver):
    deb = driver.bot.find_href("/deck/deck_index")
    driver.execute_script("arguments[0].click();", deb)

    while driver.bot.page() == '/arena/battle_index':
        time.sleep(0.1)

    print("page changed")


def change_deck(driver):
    driver.bot.refocus_frame()

    try:
        bdc = driver.find_element(By.ID, "button_deck_change_2")
        print('deck 2 clickable')
    except NoSuchElementException:
        bdc = driver.find_element(By.ID, "button_deck_change_3")
        print('deck 3 clickable')

    driver.execute_script("arguments[0].click();", bdc)
    WebDriverWait(driver, 10).until(ec.staleness_of(bdc))

    while driver.bot.page() == '/deck/deck_index':
        driver.execute_script("app.back();")


# PRINTS ALL VISIBLE OPPONENT NAMES


# iterate opponent frames
# check the frame text to confirm not an advancement battle
# get opponent name
# click frame to fight that opponent


# PRINTS FINAL ATTACK AND/OR DEF RESULTS
# on page '/arena/user_result'
# driver.switch_to.parent_frame()
# WebDriverWait(driver, 10).until(
#     ec.frame_to_be_available_and_switch_to_it((By.ID, "game_frame")))
# shadows = driver.execute_script("return document.querySelectorAll('.shadow');")
# print(shadows[1].text)