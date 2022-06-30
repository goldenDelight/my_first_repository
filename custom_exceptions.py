class NoProgressException(Exception):
    """Raised when clicking canvas no longer reduces stamina"""

    def __init__(self):
        super().__init__()
        print("no progress exception raised", end='\r', flush=True)


class MaxCardLimitException(Exception):
    """Raised when card-limit-reached redirect is confirmed"""

    def __init__(self):
        super().__init__()
        print("max card limit exception raised", end='\n', flush=True)


class NotEnoughStaminaException(Exception):
    """Raised when presence of 'not enough stamina' pop-up is confirmed"""

    def __init__(self):
        super().__init__()
        print("not enough stamina exception raised", end='\r', flush=True)


class RequestError0(Exception):
    """Raised when 'request error(0)' text in game frame"""

    def __init__(self):
        super().__init__()
        print("request error detected", end='\n', flush=True)


class ShopBreakException(Exception):
    """Raised when breaking the shackles of capitalism"""

    def __init__(self):
        super().__init__()
        print("well done comrade", end='\n', flush=True)
