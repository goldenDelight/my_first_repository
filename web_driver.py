import time

from selenium.common.exceptions import (
    TimeoutException, ElementClickInterceptedException, ElementNotInteractableException)
from selenium.webdriver.chrome.webdriver import WebDriver

import startup
import wd

main_account = {"email": "11throwaway.23@gmail.com",
                "password": "skateboard",
                "username": "Goldendlite"}
test_account = {"email": "sk8pirate24@gmail.com",
                "password": "skateboard",
                "username": "lonelybum"}


class CustomDriver(WebDriver):
    def __init__(self, main=True):
        super().__init__()
        self.get("https://www.nutaku.net/games/taimanin-asagi-battle-arena/play/")

        # startup sequence for game: login, change scope to game_frame, start

        if main:
            self.account = main_account
        else:
            self.account = test_account

        try:
            startup.log_in(self)
            startup.game_start(self)
        except Exception:
            pass

        self.ignore = (ElementClickInterceptedException,
                       ElementNotInteractableException,
                       TimeoutException)

        self.starting_bp_pots_count = 0
        self.bp_pot_count = 0
        self.initial_bp = 0
        self.initial_bp_cooldown = 0
        self.current_stam = 0

        self.boss_name = None
        self.last_boss = None

        self.slayer_battle_log = {}

        self.demon_count = [time.time()]
        self.oni_count = [time.time()]
        self.fulst_count = [time.time()]
        self.yatsu_count = [time.time()]
        self.bone_count = [time.time()]
        self.beast_count = [time.time()]

        self.arena_event_points: int = 0
        self.arena_event_fight_count: int = 0
        self.arena_event_loss_count: int = 0

    def set_arena_event_points(self, points):
        self.arena_event_points = points

    def get_arena_event_points(self):
        return self.arena_event_points

    def set_arena_event_fight_count(self, points):
        self.arena_event_fight_count = points

    def get_arena_event_fight_count(self):
        return self.arena_event_fight_count

    def set_arena_event_loss_count(self, points):
        self.arena_event_loss_count = points

    def get_arena_event_loss_count(self):
        return self.arena_event_loss_count

    def page(self):
        return wd.page(self)

    def bp_pot_tracker(self, count):
        return wd.bp_pot_tracker(self, count)

    def bp_cooldown(self):
        return wd.bp_cooldown(self)

    def current_bp(self):
        return wd.current_bp(self)

    def click(self, search_type, search_value):
        wd.click(self, search_type, search_value)

    def find(self, search_type, search_value, parent=None):
        wd.find(self, search_type, search_value, parent)

    def wait_for(self, locator, value, t=5, parent=None):
        wd.wait_for(self, locator, value, t, parent)

    def find_href(self, substring):
        wd.find_href(self, substring)

    def find_substring(self, sub_str, parent=None):
        wd.find_substring(self, sub_str, parent)

    def search_cycle(self, locator, value=None, parent=None):
        wd.search_cycle(self, locator, value, parent)

    def set_boss_name(self):
        wd.set_boss_name(self)

    def get_bp_pot_count(self):
        wd.get_bp_pot_count(self)

    def refresh_frame(self):
        wd.refresh_frame(self)


def print_temp(_str, temp=True):
    wd.print_temp(_str, temp)


def tb():
    wd.tb()


def animated_text(stall_text, wait=13, interval=1):
    wd.animated_text(stall_text, wait=13, interval=1)
