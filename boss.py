from selenium.common.exceptions import TimeoutException

import taba_bot

hp_bar_css = ('.hp_frame_top > div:nth-child(1) > div:nth-child(2) > '
              'div:nth-child(2) > div:nth-child(1)')
global name
global hp


def set_hp(driver):
    global hp
    try:
        hp_bar = driver.bot.find('css', hp_bar_css).get_attribute('style')
        hp = int((hp_bar.split()[-1])[:-2])
    except TimeoutException as e:
        taba_bot.my_traceback()
        taba_bot.print_temp(e.__class__)
        hp = 1
    return True


def set_name(driver):
    global name
    name = driver.bot.find('css', '.quest_boss_status_1').text
    return True


def get_name():
    global name
    return name


def get_hp():
    global hp
    return hp
