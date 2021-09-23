from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import taba_bot

m = "gifts"


# TODO:
#  Fix gift boss_recon stop repeat navs/not claiming gifts 1st try
#  Track claimed gifts: pots, kiryuu, etc.
#  Add check for full inventory when claiming cards


def claim_all(driver):
    driver.bot.click('class', 'decision_button_column_1')

    try:
        WebDriverWait(driver, 3).until(
            ec.visibility_of_element_located((By.ID, 'modal-win-inner')))
        popup = driver.find_element_by_id('modal-win-inner')

        c = popup.find_element_by_tag_name('a')
        driver.execute_script("arguments[0].click();", c)

    except Exception: pass


def full_inventory(driver):
    return driver.bot.find_substring("You have unclaimed_gifts gifts.") is None


def get_gifts(driver):
    driver.bot.click('class', 'decision_button_column_1')
    driver.bot.click('class', 'back_button_column_1')
    driver.bot.boss_name = None
    print("driver.bot.boss_name = None")
