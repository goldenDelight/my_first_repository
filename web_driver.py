import time

from selenium.common.exceptions import (
    TimeoutException, ElementClickInterceptedException, ElementNotInteractableException)
from selenium.webdriver.chrome.webdriver import WebDriver

import startup
import web_driver_methods

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
        return web_driver_methods.page(self)

    def bp_pot_tracker(self, count):
        return web_driver_methods.bp_pot_tracker(self, count)

    def bp_cooldown(self):
        return web_driver_methods.bp_cooldown(self)

    def current_bp(self):
        return web_driver_methods.check_current_bp(self)

    def click(self, search_type, search_value):
        web_driver_methods.click(self, search_type, search_value)

    def find(self, search_type, search_value, parent=None):
        web_driver_methods.find(self, search_type, search_value, parent)

    def wait_for(self, locator, value, t=5, parent=None):
        web_driver_methods.wait_for(self, locator, value, t, parent)

    def find_href(self, substring):
        web_driver_methods.find_href(self, substring)

    def find_substring(self, sub_str, parent=None):
        web_driver_methods.find_substring(self, sub_str, parent)

    def search_cycle(self, locator, value=None, parent=None):
        web_driver_methods.search_cycle(self, locator, value, parent)

    def get_bp_pot_count(self):
        web_driver_methods.get_bp_pot_count(self)

    def refresh_frame(self):
        web_driver_methods.refresh_frame(self)

    def refocus_frame(self):
        web_driver_methods.refocus_frame(self)


def print_temp(_str, temp=True):
    web_driver_methods.print_temp(_str, temp)


def tb():
    web_driver_methods.tb()


def animated_text(stall_text, wait=13, interval=1):
    web_driver_methods.animated_text(stall_text, wait=13, interval=1)
