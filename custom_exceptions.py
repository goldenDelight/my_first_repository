class NoProgressException(Exception):
    """Raised when clicking canvas no longer reduces stamina"""

    def __init__(self):
        super().__init__()
        print("no progress exception raised")


class MaxCardLimitException(Exception):
    """Raised when card-limit-reached redirect is confirmed"""

    def __init__(self):
        super().__init__()
        print("max card limit exception raised")


class NotEnoughStaminaException(Exception):
    """Raised when presence of 'not enough stamina' pop-up is confirmed"""

    def __init__(self):
        super().__init__()
        print("not enough stamina exception raised")


class RequestError0(Exception):
    """Raised when 'request error(0)' text in game frame"""

    def __init__(self):
        super().__init__()
        print("request error detected")


class WtfException(Exception):
    """Raised when wtf?!"""

    def __init__(self):
        super().__init__()
        print("wtf")


class ShopBreakException(Exception):
    """Raised when breaking the shackles of capitalism"""

    def __init__(self):
        super().__init__()
        print("well done comrade")
