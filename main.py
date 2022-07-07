from threading import Thread
import threading
import battle_log
import custom_driver
import quest
import vanquish_event
import nav
import tower_event
import utilities
import output
import startup
import gifts
import logic
import battle
import taba_bot
import discipline_module
from threading import Thread
import arena_event
import custom_exceptions
from custom_exceptions import ShopBreakException
import selenium
import sys

from selenium.common.exceptions import StaleElementReferenceException

import custom_driver
import quest
import tower_event
import vanquish_event
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

    print("DONE WITH GRINDING THREADS THANKS YOU GOODBYE NOW ;)", flush=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    driver = custom_driver.CustomDriver()

    t1 = Thread(group=None,
                target=alt_thread,
                name=None,
                args=(driver,),
                kwargs={},
                daemon=None)
    t1.run()

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


