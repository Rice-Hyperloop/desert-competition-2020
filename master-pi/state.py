from enum import Enum

class State(Enum):
    SAFE_TO_APPROACH = 0
    READY_TO_LAUNCH = 1
    LAUNCHING = 2
    COASTING = 3
    BRAKING = 4
    CRAWLING = 5
    FAULT = 6
