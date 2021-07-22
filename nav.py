from selenium.common.exceptions import JavascriptException, TimeoutException, StaleElementReferenceException, \
    NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

import web_driver
from handlers import MaxCardLimitException, RequestError0, ShopBreakException


# def battle(driver):
#     try:
#         if driver.find_element_by_id("main_frame_raid_on_bg"):
#             battle_page(driver)
#         elif driver.find_element_by_id("main_frame"):
#             raid_boss_list(driver)
#             battle_page(driver)
#     except NoSuchElementException:
#         pass

# def check_page(driver, title):
#     # var location_url
#
#     try:
#         driver.wait_for('id', 'page_title_text')
#         WebDriverWait(driver, 3).until(ec.visibility_of_element_located((By.ID, "page_title_text")))
#         page = driver.execute_script("return document.querySelector('#page_title_text')")
#         return title in page.text
#
#     except (AttributeError, TimeoutException):
#         import startup
#         top_page = driver.find_substring("Top Page")
#         if top_page is not None:
#             driver.execute_script("arguments[0].click();", top_page)
#         elif driver.find_element_by_id("gadget_contents").text == 'Request Error(0)':
#             driver.execute_script("gadgets.util.runOnLoadHandlers();")
#         startup.game_start(driver)
#     except StaleElementReferenceException:
#         pass


def boss_alert(driver):
    if driver.page() == "/mypage/index":
        try:
            WebDriverWait(driver, 3).until(ec.element_to_be_clickable((By.ID, "boss_alerts_1")))
            alert = driver.find_element_by_id("boss_alerts_1")
            return alert is not None
        except (JavascriptException, TimeoutException):
            return False


def main_page(driver, force_refresh=False):
    try:
        if driver.page() == "/item/item_shop":
            raise ShopBreakException
        elif driver.page() != "/mypage/index" or force_refresh:
            driver.click("id", "mypage")
    except JavascriptException:
        raise JavascriptException


def slayer_event_page(driver):
    if driver.page() == "/mypage/index":
        hunt = driver.execute_script(
            "return document.querySelector('a[href*=hunt_event_top]');")
        driver.execute_script("arguments[0].click();", hunt)

        WebDriverWait(driver, 5).until(ec.presence_of_all_elements_located(
            (By.CLASS_NAME, "hexagon_button")))


# Only for Slayer Events
def battle_to_event_stage(driver):
    WebDriverWait(driver, 5).until(ec.visibility_of_element_located(
        (By.ID, "hunt_result")))

    try:
        pts = driver.execute_script("return document.querySelector('#hunt_"
                                    "result > div > div:nth-child(5) > div > "
                                    "div:nth-child(6)');").text
        pts = pts.split("\u3000")[-1]
        web_driver.print_temp(pts, False)

    except Exception:
        pass

    result = driver.find_element_by_id("hunt_result")
    close = result.find_element_by_class_name("closePopup")
    driver.execute_script("arguments[0].click();", close)

    WebDriverWait(driver, 5).until(ec.presence_of_all_elements_located(
        (By.TAG_NAME, "a")))

    hunt = driver.execute_script(
        "return document.querySelector('a[href*=hunt_start]');")

    driver.execute_script("arguments[0].click();", hunt)
    WebDriverWait(driver, 5).until(ec.staleness_of(hunt))


def battle_page(driver, slayer_event=False):

    if slayer_event or raid_boss_list(driver):

        try:
            WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located(
                (By.CLASS_NAME, "friend_frame")))

            friend_frames = driver.find_elements_by_class_name("friend_frame")
            ranking_frames = driver.find_elements_by_class_name("ranking_frame")
            container = driver.find_element_by_id("scroll_content")

            for frame in friend_frames:
                driver.execute_script("arguments[0].scrollTop=arguments[1].offsetTop", container, frame)
                info = frame.text.split("\n")

                if driver.account.get("username") in info[-2]:
                    driver.execute_script("arguments[0].click();", frame)
                    WebDriverWait(driver, 3).until(ec.staleness_of(frame))
                    return driver.page() == "/raid/boss_arrival"

        except (IndexError, TimeoutException):
            pass

        return False

    else:
        return False


def quest_to_boss_list(driver, slayer_event=False):
    if slayer_event or driver.page() == "/quest/quest_start":
        cvs = driver.find_element_by_id("canvas")
        ActionChains(driver).move_to_element_with_offset(
            driver.find_element_by_id("gadget_contents"), 200, 300).click().perform()
        WebDriverWait(driver, 3).until(ec.staleness_of(cvs))
    if driver.page() == "/card/card_max":
        raise MaxCardLimitException


def raid_boss_list(driver):
    if driver.page() == "/raid/raid_index":
        return True
    elif driver.page() == "/card/card_max":
        raise MaxCardLimitException

    try:
        main_page(driver)
        driver.click("id", "boss_alerts_1")
    except NoSuchElementException:
        return False

    return driver.page() == "/raid/raid_index"


def quest(driver):
    try:
        driver.click("class", "top_menu_1")

        if driver.page() == "/card/card_max":
            raise MaxCardLimitException

        WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.ID, "chapter1")))
        chapter1 = driver.find_element_by_id("chapter1")
        driver.execute_script("arguments[0].click()", chapter1)

        WebDriverWait(driver, 3).until(ec.presence_of_element_located((By.ID, "stage1-link")))
        stage1 = driver.find_element_by_id("stage1-link")
        driver.execute_script("arguments[0].click()", stage1)

        WebDriverWait(driver, 3).until(ec.visibility_of_element_located((By.ID, "canvas")))

    except NoSuchElementException:
        if driver.find_element_by_id("gadget_contents").text == 'Request Error(0)':
            raise RequestError0
    except MaxCardLimitException:
        raise MaxCardLimitException


def event_page(driver):
    try:
        main_page(driver)
        driver.click("css", "#main_frame > a:nth-child(7)")
        return True
    except Exception:
        web_driver.tb()

    return False


def event_stage(driver):
    WebDriverWait(driver, 5).until(ec.presence_of_all_elements_located((By.TAG_NAME, "a")))
    anchors = driver.execute_script("return document.querySelectorAll('a');")
    for a in anchors:
        if ((a.get_attribute("onClick") == "app.back();") or (
                "hunt_start" in a.get_attribute("href"))):
            driver.execute_script("arguments[0].click();", a)
            WebDriverWait(driver, 10).until(ec.staleness_of(a))
            break


def gifts(driver):
    driver.click("class", "button-present")
    if driver.page() == "/card/card_max":
        raise MaxCardLimitException
    else:
        return driver.page() == "/present/index"


def unclaimed_gifts(driver):
    main_page(driver)

    try:
        WebDriverWait(driver, 3).until(ec.visibility_of_element_located(
            (By.CLASS_NAME, "button-present")))
        gifts_button = driver.find_element_by_class_name("button-present")
        icon_url = gifts_button.get_attribute('style').split('"')[1]
        return "present_2" in icon_url

    except AttributeError:
        web_driver.tb()
    except StaleElementReferenceException:
        web_driver.tb()
    except TimeoutException:
        if driver.find_element_by_id("gadget_contents").text == 'Request Error(0)':
            driver.refresh_frame()


def boss_recon(driver):
    status = WebDriverWait(driver, 3).until(ec.presence_of_all_elements_located(
        (By.CLASS_NAME, "quest_boss_status_1")))
    name = status[0].text
    if "(AR)" in name:
        web_driver.print_temp("fighting AR", False)

    if driver.boss_name is None:
        driver.boss_name = name
        import output
        output.boss_counter(driver)


def defeat_retry(driver):
    buttons = WebDriverWait(driver, 5).until(
        ec.presence_of_all_elements_located(
            (By.CLASS_NAME, "decision_button_column_1")))

    for b in buttons:
        if "Retry" in b.text:
            driver.execute_script("arguments[0].click();", b)
            WebDriverWait(driver, 5).until(ec.staleness_of(b))
            break
