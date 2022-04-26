from threading import Thread

from selenium.common.exceptions import (StaleElementReferenceException)

import custom_driver
import quest
import tower_event
from custom_exceptions import ShopBreakException


def alt_thread(driver):

    while True:
        try:
            flow.vanquish_event(driver)
            tower_event.grind(driver)
            flow.grind(driver)
            # grind(driver)
            # flow.event_grind(driver)
            flow.grind(driver)
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
