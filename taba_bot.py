import re
import time

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    UnexpectedAlertPresentException,
    JavascriptException,
    StaleElementReferenceException, WebDriverException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


search_syntax_dic = {
    'css': By.CSS_SELECTOR,
    'xpath': By.XPATH,
    'id': By.ID,
    'tag': By.TAG_NAME,
    'class': By.CLASS_NAME,
    'name': By.NAME
}

find_syntax_dic = {
    'id': (lambda a, b: a.find_element_by_id(b)),
    'tag': (lambda a, b: a.find_element_by_tag_name(b)),
    'class': (lambda a, b: a.find_element_by_class_name(b)),
    'name': (lambda a, b: a.find_element_by_name(b)),
    'css': (lambda a, b: a.find_element_by_css_selector(b))
}


class Bot:

    def __init__(self, driver):
        import utilities
        utilities.last_message = ""

        self.driver = driver

        self.bp_pot_count = 0
        self.initial_bp = 0
        self.initial_bp_cooldown = 0

        self.boss_name = None

        self.slayer_battle_log = {}

        self.demon_count = [time.time()]
        self.oni_count = [time.time()]
        self.fulst_count = [time.time()]
        self.yatsu_count = [time.time()]
        self.bone_count = [time.time()]
        self.beast_count = [time.time()]

        self.arena_event_points: int = 0
        self.arena_event_fight_count: int = 0
        self.arena_event_loss_count: int = 0

    def page(self):
        try:
            page = self.driver.execute_script("return location_url")
            # print(f"u at {page} bitch")
            return page

        except JavascriptException:
            self.driver.switch_to.parent_frame()
            WebDriverWait(self.driver, 10).until(
                ec.frame_to_be_available_and_switch_to_it(
                    (By.ID, 'game_frame')))

    # def bp_pot_tracker(self, count):
    #     self.bp_pot_count = count
    #     if self.driver.starting_bp_pots_count == 0:
    #         self.driver.starting_bp_pots_count = count
    #     return None

    def click(self, search_key, search_value):
        try:
            WebDriverWait(self.driver, 3).until(
                ec.element_to_be_clickable(
                    (search_syntax_dic.get(search_key), search_value)))
        except TimeoutException:
            pass

        try:
            get = find_syntax_dic.get(search_key)
            element = get(self.driver, search_value)
            self.driver.execute_script("arguments[0].click();", element)
            WebDriverWait(self.driver, 3).until(ec.staleness_of(element))

        except NoSuchElementException:
            if self.driver.find_element_by_id(
                    'gadget_contents').text == "Request Error(0)":
                self.refresh_frame()

        except TimeoutException:
            from utilities import print_temp
            print_temp("element not stale")

        return None

    def find_href(self, substring):
        WebDriverWait(self.driver, 3).until(
            ec.presence_of_all_elements_located((By.TAG_NAME, 'a')))

        anchors = self.driver.execute_script(f"return document.querySelectorAll('a')")

        for a in anchors:
            if substring in str(a.get_attribute('href')):
                return a

    def find_substring(self, sub_str, parent=None):
        parent = self.driver if parent is None else parent
        try:
            WebDriverWait(self.driver, 3).until(ec.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(), '{sub_str}')]")))
            return parent.find_element_by_xpath(
                f"//*[contains(text(), '{sub_str}')]")
        except TimeoutException:
            return None

    def search_cycle(self, locator, value=None, parent=None):
        import time
        parent = self.driver if parent is None else parent
        for i in range(15):
            try:
                if value is None:
                    return self.driver.execute_script(locator)
                else:
                    parent.find_element(locator, value)
            except NoSuchElementException:
                pass
            except UnexpectedAlertPresentException:
                pass
            except JavascriptException:
                pass
            except StaleElementReferenceException:
                print("stale element reference exception")

            time.sleep(0.1)
        return None

    def bp_cooldown(self):
        try:
            bp_text = self.driver.execute_script(
                "return document.getElementById('bp_gage_time').innerText")[-2:]
            cd = int(bp_text)
            print(f"bp cooldown: {cd % 20}")
            return cd % 20
        except JavascriptException:
            from utilities import my_traceback
            my_traceback()
            if self.driver.find_element_by_id(
                    'gadget_contents').text == "Request Error(0)":
                self.refresh_frame()

    def check_current_bp(self):
        try:
            if curr_bp := self.driver.execute_script(
                    "return document.getElementById('top_bp_num').innerText")[0]:
                return int(curr_bp)

        except JavascriptException:
            from utilities import my_traceback
            my_traceback()
            if self.driver.find_element_by_id(
                    'gadget_contents').text == "Request Error(0)":
                self.refresh_frame()
            return None

        except WebDriverException:
            from utilities import my_traceback, print_temp

            my_traceback()
            print_temp(
                "Unable to get 'innerText' of undefined or null ref.", False)

    def refresh_frame(self):
        self.driver.execute_script("gadgets.util.runOnLoadHandlers();")
        import startup
        startup.game_start(self.driver)
        return None

    def refocus_frame(self):
        self.driver.switch_to.parent_frame()
        WebDriverWait(self.driver, 10).until(
            ec.frame_to_be_available_and_switch_to_it((By.ID, 'game_frame')))

    def find(self, search_type, search_value, parent=None):
        locator = search_syntax_dic.get(search_type)
        element = self.search_cycle(locator, search_value, parent)
        return element

    def wait_for(self, locator, value, t=5, parent=None):
        locator = search_syntax_dic.get(locator)
        parent = self.driver if parent is None else parent
        element = None

        try:
            element = WebDriverWait(parent, t).until(
                ec.element_to_be_clickable((locator, value)))
        except TimeoutException:
            try:
                element = WebDriverWait(parent, t).until(
                    ec.visibility_of_element_located((locator, value)))
            except TimeoutException:
                pass

        return element

    @property
    def get_bp_pot_count(self):
        self.click('class', 'top_menu_7')
        btns = self.driver.find_elements_by_class_name(
            'decision_button_column_2')
        self.driver.execute_script("arguments[0].click();", btns[2])

        WebDriverWait(self.driver, 4).until(ec.staleness_of(btns[2]))

        items = self.driver.find_elements_by_class_name('item_shop_description')
        self.driver.bp_pot_count = re.sub('[^0-9]', "", items[16].text)
        print(self.driver.bp_pot_count)

        if self.driver.starting_bp_pots_count is None:
            self.starting_bp_pots_count = self.bp_pot_count
        return None


