from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

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
        popup = driver.find_element(By.ID, 'modal-win-inner')

        c = popup.find_element(By.TAG_NAME, 'a')
        driver.execute_script("arguments[0].click();", c)

    except Exception: pass


def full_inventory(driver):
    return driver.bot.find_substring("You have unclaimed_gifts gifts.") is None


def get_gifts(driver):
    driver.bot.click('class', 'decision_button_column_1')
    driver.bot.click('class', 'back_button_column_1')
    driver.bot.boss_name = None
    print("driver.bot.boss_name = None")

# event rank elements
#
# main page 'rank rewards available' gifts button icon
# background-image: url("https://cf.tna.dmmgames.com/img/pc/system/button/present_Event_Rewards_NEW.png"); opacity: 1;
#
# gifts landing page href to collect event rewards
# href="/event_ranking_reward/index"
#
# event rank reward page
# '/event_ranking_reward/index'
#
# href="/event_ranking_reward/send_all_to_gift"
#
# element displaying final event rank on the rewards page
# <div id="rank"> (int) </div>