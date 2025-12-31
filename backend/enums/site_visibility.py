from enum import Enum

class SiteVisibility(str, Enum):
    Perfect = "Perfect"     # > 99%
    Amazing = "Amazing"     # 90-99%
    Great = "Great"         # 80–90%
    Good = "Good"           # 60–80%
    Ok = "Ok"               # 50–60%
    Bad = "Bad"             # 30–50%
    Terrible = "Terrible"   # < 30%