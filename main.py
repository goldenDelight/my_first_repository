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
import logging
import threading
import time
from functools import wraps

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

import arena_event
import battle_log
import custom_driver
import quest
import vanquish_event
import nav
import tower_event
from tower_event import TowerEvent
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
from selenium.common.exceptions import (StaleElementReferenceException)
import selenium
import sys


def main_grinder(tower, driver):
    try:
        while input("continue? (y/n)\n") == "y":
            tower.grind(driver)
    except:
        main_grinder(tower, driver)

# def alt_thread(t_driver):
#     tower = tower_event.TowerEvent()
#     tower.quota = 10000000
#
#     shop_break = False
#
#     while not shop_break:
#         try:
#             if tower.event_points < tower.quota:
#                 tower.grind(t_driver)
#             else:
#                 quest.grind(t_driver)
#
#         except ShopBreakException:
#             shop_break = True
#             break
#         except:
#             pass
#
#     print("DONE WITH GRINDING THREADS THANKS YOU GOODBYE NOW ;)")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver = custom_driver.CustomDriver('main')
    tower = tower_event.TowerEvent()
    tower.quota = 10000000

    try:
        main_grinder(tower, driver)
    except:
        input("kk something got fucked up")
        pass

    # t1 = Thread(group=None,
    #             target=alt_thread,
    #             name=None,
    #             args=(driver,),
    #             kwargs={},
    #             daemon=None)
    # t1.run()



    # driver = custom_driver.CustomDriver()
    #
    # t1 = Thread(group=None,
    #             target=alt_thread,
    #             name=None,
    #             args=(driver,),
    #             kwargs={},
    #             daemon=None)
    # t1.run()
