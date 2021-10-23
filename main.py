import time
from threading import Thread

from selenium.common.exceptions import (StaleElementReferenceException)
import flow
from custom_exceptions import ShopBreakException
import custom_driver
from tower_event import tower_event_grind
# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code. Press Double
# Shift to search everywhere for classes, files, tool windows, actions,
# and settings.


def alt_thread(driver):

    while True:
        try:
            # tower_event_grind(driver)
            # flow.is_event(driver)
            flow.grind_routine(driver)
        except StaleElementReferenceException:
            pass
        except ShopBreakException:
            break

    print("DONE WITH GRINDING THREADS THANKS YOU GOODBYE NOW ;)")


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
