from selenium.common.exceptions import TimeoutException

import web_driver

hp_bar_css = (".hp_frame_top > div:nth-child(1) > div:nth-child(2) > "
              "div:nth-child(2) > div:nth-child(1)")
global name
global hp


def set_hp(driver):
    f = "hp"
    global hp
    try:
        hp_bar = driver.find("css", hp_bar_css).get_attribute("style")
        hp = int((hp_bar.split()[-1])[:-2])
    except TimeoutException as e:
        web_driver.tb()
        web_driver.print_temp(e.__class__)
        hp = 1
    return True


def set_name(driver):
    global name
    name = driver.find("css", ".quest_boss_status_1").text
    return True


def get_name():
    global name
    return name


def get_hp():
    global hp
    return hp
