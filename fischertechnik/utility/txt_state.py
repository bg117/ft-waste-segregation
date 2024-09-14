from enum import Enum

class TxtState(Enum):
    TRANSFERRING = "T"
    INIT = "I"
    STOP = "S"
    RUNNING = "R"
    FINALIZING = "F"
    INTERFACE_TEST_START = "D"
    INTERFACE_TEST_STOP = "E"
