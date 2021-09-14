import time

import selenium.webdriver.support.expected_conditions as ec
from selenium.common.exceptions import (
    StaleElementReferenceException,
    ElementClickInterceptedException,
    TimeoutException, NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import \
    visibility_of_element_located as ec_visible
from selenium.webdriver.support.wait import WebDriverWait

import nav
import utilities
import web_driver
from handlers import MaxCardLimitException
from handlers import NoProgressException
from handlers import NotEnoughStaminaException

canvas: WebElement
stam_bar: WebElement
pre_click_stam: int
current_stam: int
loading_box: WebElement


def initialize_vars(driver) -> None:
    global canvas, stam_bar, pre_click_stam, current_stam

    web_driver.print_temp("initializing grind vars")

    WebDriverWait(driver, 5).until(ec_visible((By.ID, 'canvas')))

    canvas = driver.execute_script("return document.querySelector('#canvas');")
    stam_bar = driver.execute_script(
        "return document.querySelector('#stam_gage_num');")

    if stam_bar is not None:
        pre_click_stam = int(stam_bar.text.split("/")[0])
        current_stam = 0


def grind(driver, slayer_event=False):
    global canvas, loading_box, stam_bar, pre_click_stam, current_stam

    try:
        loading_box = driver.find_element_by_id('loadingbox')
        WebDriverWait(driver, 10).until(ec.staleness_of(loading_box))
    except NoSuchElementException:
        pass
    except TimeoutException:
        WebDriverWait(driver, 10).until(ec.staleness_of(loading_box))

    WebDriverWait(driver, 5).until(ec_visible((By.ID, 'page_title_text')))
    initialize_vars(driver)

    while pre_click_stam >= current_stam:
        try:
            pre_click_stam = int(stam_bar.text.split("/")[0])
            click_cycle()
        except TimeoutException: break
        except StaleElementReferenceException:
            initialize_vars(driver)
        except AttributeError:
            try:
                canvas = driver.execute_script(
                    "return document.querySelector('#canvas');")
                canvas.click()
            except StaleElementReferenceException: break
            except AttributeError: break
        except NoProgressException:
            web_driver.print_temp("ending grind sequence")
            break
        except NotEnoughStaminaException:
            utilities.use_stam(driver)
            if not slayer_event:
                nav.quest(driver)
            else:
                nav.event_page(driver)
                nav.event_stage(driver)


def click_cycle():
    global stam_bar, pre_click_stam

    for i in range(12):
        bar_value = int(stam_bar.text.split('/')[0])
        try:
            if bar_value >= pre_click_stam:
                canvas.click()
                time.sleep(.75)
            if int(stam_bar.text.split('/')[0]) - pre_click_stam > 2:
                raise NoProgressException
        except ElementClickInterceptedException:
            raise NotEnoughStaminaException
        except AttributeError:
            raise MaxCardLimitException

    if pre_click_stam <= int(stam_bar.text.split('/')[0]):
        raise NoProgressException
