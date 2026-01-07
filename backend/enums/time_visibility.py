from enum import Enum

class TimeVisibility(str, Enum):
    NOW = "Now"
    TONIGHT = "Tonight"
    TOMORROW_NIGHT = "Tomorrow Night"
    NIGHTS_3_FROM_NOW = "Three Nights From Now"