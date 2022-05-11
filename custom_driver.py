from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    ElementNotInteractableException)
from selenium.webdriver.chrome.webdriver import WebDriver
# from seleniumwire import webdriver

import arena_event
import battle
import battle_log
import custom_exceptions
import discipline_module
import quest
import gifts
import logic
import nav
import output
import stage
import startup
import taba_bot
import tower_event
import utilities
import vanquish_event

main_account = {"email": "11throwaway.23@gmail.com",
                "password": "skateboard",
                "username": "Goldendlite"}

test_account = {"email": "sk8pirate24@gmail.com",
                "password": "skateboard",
                "username": "lonelybum"}


class CustomDriver(WebDriver):
    def __init__(self):
        super().__init__()
        self.get(
            "https://www.nutaku.net/games/taimanin-asagi-battle-arena/play/")

        # startup sequence for game: login, change scope to game_frame, start

        self.bot = taba_bot.Bot(self)

        self.ignore = (ElementClickInterceptedException,
                       ElementNotInteractableException,
                       TimeoutException)
        self.account = main_account

        try:
            startup.log_in(self)
            startup.game_start(self)
        except Exception:
            pass

    def make_new_bot(self):
        from importlib import reload
        reload(taba_bot)
        reload(stage)
        reload(utilities)
        reload(gifts)
        reload(battle)
        reload(quest)
        reload(nav)
        reload(logic)
        reload(output)
        reload(tower_event)
        reload(startup)
        reload(discipline_module)
        reload(battle_log)
        reload(arena_event)
        reload(vanquish_event)
        reload(custom_exceptions)

        self.bot = taba_bot.Bot(self)
