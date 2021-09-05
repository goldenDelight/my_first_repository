import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


# nav to Discipline main page
def nav_to_discipline(driver):
    links = driver.execute_script("return document.querySelectorAll('a');")
    for link in links:
        if "compose_index?" in link.get_attribute('href'):
            driver.execute_script("arguments[0].click();", link)
        elif "compose_index" in link.get_attribute('href'):
            driver.execute_script("arguments[0].click();", link)


# filters list to display specific rank cards (default is "N" rank)
def display_cards_by_rank(driver, rank="N"):
    rank_index = {"All": 0,
                  "N": 1,
                  "R": 2,
                  "HR": 3,
                  "SR": 4,
                  "UR": 5,
                  "LR": 6, }

    rarity_selector = Select(driver.execute_script("return document.querySelector('#select_filter_rare');"))
    rarity_selector.select_by_index(rank_index.get(rank))


def confirm_has_xp_fodder(driver):
    frames = driver.execute_script(
        "return document.querySelectorAll('.compose_card_frame');")
    if frames.__len__() <= 1:
        return False
    else:
        return True


# 10x loop clicking first card displayed, then clicks confirm button
def select_xp_fodder_cards(driver):
    for i in range(10):
        fodder = driver.execute_script("return document.querySelector('#card_image');")
        driver.execute_script("arguments[0].click();", fodder)


# Triggers discipline action, waits 3s for button staleness before returning
def trigger_discipline_event(driver):
    discipline = driver.execute_script("return document.querySelector('#button_compose_confirm');")
    driver.execute_script("arguments[0].click();", discipline)

    try:
        WebDriverWait(driver, 3).until(ec.staleness_of(discipline))
    except TimeoutException:
        pass


def skip_animation(driver):
    while driver.page() == '/compose/compose_index':
        try:
            ActionChains(driver).move_to_element_with_offset(
                driver.find_element_by_id("gadget_contents"), 450, 675).click().perform()

            time.sleep(0.5)

        except:
            break


def check_under_leveled(driver):
    card_info = driver.execute_script(
        "return document.querySelector('#main_frame_compose > div:nth-child(4) > div:nth-child(3)');")

    if card_info.text == 'Lv:\nATK:\nDEF:':
        return False
    else:
        return True


def assisted_levelling(driver):
    if "compose_index" in driver.page():
        display_cards_by_rank(driver)

        if confirm_has_xp_fodder(driver):
            select_xp_fodder_cards(driver)
            trigger_discipline_event(driver)
            skip_animation(driver)
            nav_to_discipline(driver)
            return True
        else:
            return False
    else:
        return False
