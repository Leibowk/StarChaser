from datetime import datetime, time, timedelta
from typing import Optional
from enums.time_visibility import TimeVisibility

class DateTimeService:
    def date_time_helper(self, time_visibility: Optional[TimeVisibility]) -> datetime:
        """
        Returns a datetime object based on the TimeVisibility enum.
        
        Rules:
        - None -> tonight at 10 PM
        - NOW -> forecast datetime
        - TONIGHT -> tonight at 10 PM
        - TOMORROW_NIGHT -> tomorrow at 10 PM
        - NIGHTS_3_FROM_NOW -> 3 nights from today at 10 PM
        """

        now = datetime.now()
        target_time = time(22, 0)  # 10:00 PM

        if time_visibility is None:
            return datetime.combine(now.date(), target_time)

        if time_visibility == TimeVisibility.NOW:
            return now

        if time_visibility == TimeVisibility.TONIGHT:
            return datetime.combine(now.date(), target_time)

        if time_visibility == TimeVisibility.TOMORROW_NIGHT:
            tomorrow = now.date() + timedelta(days=1)
            return datetime.combine(tomorrow, target_time)

        if time_visibility == TimeVisibility.NIGHTS_3_FROM_NOW:
            three_nights = now.date() + timedelta(days=3)
            return datetime.combine(three_nights, target_time)

        return datetime.combine(now.date(), target_time)
