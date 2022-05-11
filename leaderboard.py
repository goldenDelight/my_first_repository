from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


# accesses leaderboard from event splash page
def nav_leaderboard(driver):
    ref = driver.bot.find_href('ranking')
    driver.execute_script("arguments[0].click();", ref)
    WebDriverWait(driver, 10).until(ec.staleness_of(ref))


def find_rank(driver, rank=50):
    frames = []

    while len(frames) < rank:
        scroll_content = driver.execute_script(
            "return document.querySelector('#scroll_content');")
        scroll_content.find_elements(By.CLASS_NAME, "ranking_frame")
        scroll_content = driver.execute_script(
            "return document.querySelector('#scroll_content');")
        frames = scroll_content.find_elements(By.CLASS_NAME, "ranking_frame")
        driver.execute_script("arguments[0].scrollBy(0,1000)", scroll_content)

    return frames[rank-1]


def find_rank_points(driver):
    rank50 = driver.execute_script(
        "return document.querySelector('#ranking50');")

    points_for_rank50 = driver.execute_script(
        "return arguments[0].querySelector('#rank_point');", rank50)



