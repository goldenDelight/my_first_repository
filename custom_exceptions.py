class NoProgressException(Exception):
    """Raised when clicking canvas no longer reduces stamina"""
    print("no progress exception raised")


class MaxCardLimitException(Exception):
    """Raised when card-limit-reached redirect is confirmed"""
    print("max card limit exception raised")


class NotEnoughStaminaException(Exception):
    """Raised when presence of 'not enough stamina' pop-up is confirmed"""
    print("not enough stamina exception raised")


class RequestError0(Exception):
    """Raised when 'request error(0)' text in game frame"""
    print("request error detected")


class WtfException(Exception):
    """Raised when wtf?!"""
    print("wtf")


class ShopBreakException(Exception):
    """Raised when breaking the shackles of capitalism"""
    print("well done comrade")
