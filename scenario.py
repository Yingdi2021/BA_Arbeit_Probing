from enum import Enum

class Scenario(Enum):
    NONE = 1
    EXACT1 = 2
    THRESHOLD = 3
    ALL = 4
    NONEORALL = 5
    XOR = 6