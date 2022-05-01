from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# accesses leaderboard from event splash page
def nav_leaderboard(driver):
    ref = driver.bot.find_href('ranking')
    driver.execute_script("arguments[0].click();", ref)
    WebDriverWait(driver, 10).until(ec.staleness_of(ref))
