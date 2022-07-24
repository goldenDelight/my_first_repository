from selenium.common.exceptions import (TimeoutException,
                                        StaleElementReferenceException,
                                        ElementClickInterceptedException,
                                        NoSuchElementException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import nav
import utilities
from custom_exceptions import ShopBreakException

# global quota
# global quota_hit


class TowerEvent:

    def __init__(self, quota=0):

        self.quota = quota
        self.event_points = None
        self.quota_hit = False
        self.gacha_points = -1

    def grind(self, driver):

        while self.quota_hit is False:
            self.tower_grind(driver)

    def tower_grind(self, driver):

        if driver.bot.page() == '/mypage/index':
            nav.event_page(driver, "tower")
        elif driver.bot.page() == '/item/item_shop':
            raise ShopBreakException

        if driver.bot.page() == '/tower/tower_event_top':
            try:
                driver.find_element(By.ID, 'canvas').click()

            except NoSuchElementException:
                try:
                    stage_info = driver.execute_script(
                        "return document.getElementsByClassName("
                        "'stage_info_frame');")

                    if stage_info is not None:
                        info_text = stage_info[0].text
                        info_lines = info_text.splitlines()
                        points_str = info_lines[2]
                        self.event_points = int(points_str.split()[-1])

                        utilities.print_temp(f"points: {self.event_points:,}")

                        if self.event_points >= self.quota:
                            self.quota_hit = True
                            utilities.print_temp(f"\nHit quota!! points: {self.event_points:,}\n", temp=False)
                            return True

                except:
                    pass

        if driver.bot.page() == '/tower/tower_event_top':
            try:
                driver.find_element(By.ID, 'canvas').click()
            except NoSuchElementException:
                pass

            stage = driver.bot.find_href("tower/tower_start?chapter")
            driver.execute_script("arguments[0].click();", stage)
            WebDriverWait(driver, 3).until(ec.staleness_of(stage))

        if driver.bot.page() == '/tower/tower_start':

            if driver.bot.find_href('item/use_confirm'):
                utilities.use_stam(driver, tower_event=True)
            else:
                driver.bot.click('class', 'quest_dash_button')

        if driver.bot.page() == '/tower/tower_event_result':
            try:
                driver.find_element(By.ID, 'canvas').click()
            except (NoSuchElementException, StaleElementReferenceException):
                try:
                    driver.bot.click('class', 'decision_button_column_1')
                except StaleElementReferenceException:
                    return
            try:
                driver.find_element(By.ID, 'canvas').click()
            except (NoSuchElementException, StaleElementReferenceException, ElementClickInterceptedException):
                pass

        if driver.bot.page() == '/card/card_max':
            utilities.sell_cards(driver)
        elif driver.bot.page() == '/item/item_shop':
            raise ShopBreakException

        return False
