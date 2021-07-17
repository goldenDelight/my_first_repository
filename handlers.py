from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def restore_stam(self):
    use_small_stams = self.execute_script("return document.querySelectorAll('.decision_button_column_2")
    self.execute_script("arguments[0].click();", use_small_stams[0])

    WebDriverWait(self, 3).until(ec.staleness_of(use_small_stams))

    confirm_use = self.find_element_by_css_selector("#main_frame_item > div:nth-child(5) > a:nth-child(1)")
    self.execute_script("arguments[0].click();", confirm_use)

    WebDriverWait(self, 3).until(ec.staleness_of(confirm_use))

    return_to_event = self.find_element_by_css_selector("#main_frame_item > div:nth-child(5) > a:nth-child(1)")
    self.execute_script("arguments[0].click();", return_to_event)

    WebDriverWait(self, 3).until(ec.staleness_of(return_to_event))

#     locate, click last button to return to grind_routine
    all_anchors = self.execute_script("return document.querySelectorAll('a');")
    for a in all_anchors:
        href = a.get_attribute('href')
        if "/tower/tower_start" in href:
            self.execute_script("arguments[0].click();", a)


def card_sales(driver):
    driver.execute_script("return document.querySelector('#numbner_of_card');")
    bulk = driver.execute_script("return document.querySelector('#button_bulk');")
    driver.execute_script("arguments[0].click();", bulk)


def screen_cards(driver):
    cards_to_sell = driver.execute_script("return document.querySelectorAll('div[id^=showcase_frame]');")

    for card in cards_to_sell:
        info = driver.execute_script("return arguments[0].querySelectorAll('*');", card)
        for i in info:
            if i.get_attribute('src') == "https://cf.tna.dmmgames.com/img/common/card/S/C00040b." \
                                         "73fcabcb223e0a96e48159015766757a.png":
                print(i.get_attribute("id"))
                print(cards_to_sell.index(card))


class NoProgressException(Exception):
    """Raised when clicking canvas no longer reduces stamina"""
    print("no progress exception raised")


class MaxCardLimitException(Exception):
    """Raised when card-limit-reached redirect is confirmed"""
    print("max card limit exception raised")


class NotEnoughStaminaException(Exception):
    """Raised when presence of 'not enough stamina' pop-up is confirmed"""
    print("not enough stamina exception raised")


class RequestError0(Exception):
    """Raised when 'request error(0)' text in game frame"""
    print("request error detected")


class wtfException(Exception):
    """Raised when wtf?!"""
    print("wtf")


class ShopBreakException(Exception):
    """Raised when trying to break the chains of capitalism"""
    print("well done comrade")
