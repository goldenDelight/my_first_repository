from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    ElementNotInteractableException)
from selenium.webdriver.chrome.webdriver import WebDriver

import startup
import taba_bot

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
        self.bot = taba_bot.Bot(self)
