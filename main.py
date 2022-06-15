from threading import Thread

from selenium.common.exceptions import (StaleElementReferenceException)

import custom_driver
import quest
import tower_event
from custom_exceptions import ShopBreakException


def alt_thread(t_driver):

    quota_hit = False

    while True:
        try:
            if not quota_hit:
                quota_hit = tower_event.grind(t_driver)
            else:
                quest.grind(driver)
        except StaleElementReferenceException:
            pass
        except ShopBreakException:
            break

    print("DONE WITH GRINDING THREADS THANKS YOU GOODBYE NOW ;)")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    driver = custom_driver.CustomDriver()

    # while True:
    #     try:
    #         # arena_event.grind(driver)
    #         # vanquish_event.grind(driver)
    #         # tower_event.grind(driver)
    #         quest.grind(driver)
    #     except StaleElementReferenceException:
    #         pass
    #     except ShopBreakException:
    #         break
    #     except KeyboardInterrupt:
    #         break
    # print("DONE WITH GRINDING THREADS THANKS YOU GOODBYE NOW ;)")


