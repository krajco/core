from enum import Enum


class NagiosState(Enum):
    OK = 0
    Warning = 1
    Critical = 2
    Unknown = 3
