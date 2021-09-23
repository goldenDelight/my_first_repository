import time

from selenium.common.exceptions import (StaleElementReferenceException)
import flow
from handlers import ShopBreakException
import custom_driver

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code. Press Double
# Shift to search everywhere for classes, files, tool windows, actions,
# and settings.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    driver = custom_driver.CustomDriver()

    time.sleep(5)

    while True:
        try:
            # full_power_event_grind(driver)
            # flow.is_event(driver)
            flow.grind_routine(driver)
        except StaleElementReferenceException:
            pass
        except ShopBreakException:
            break
