import datetime as dt
from enum import Flag, auto


class Weekdays(Flag):
    MON = auto()
    TUE = auto()
    WED = auto()
    THU = auto()
    FRI = auto()
    SAT = auto()
    SUN = auto()


def count_occurrences(
    start: dt.date,
    weekdays: Weekdays,
    period: int,
    interval_start: dt.date,
    interval_end: dt.date,
):
    total = 0
    for i, weekday in enumerate(Weekdays):
        if weekday not in weekdays:
            continue

        if i < start.weekday():
            days_to_this_weekday = 7 - start.weekday() + i
        else:
            days_to_this_weekday = i - start.weekday()

        left = start + dt.timedelta(days=days_to_this_weekday)
        # left < interval_start | left <= interval_end | left > interval_end
        if left < interval_start:
            # how many same weekdays before start
            a = ((interval_start - left).days - 1) // (period * 7)
            # how many same weekdays before and including end
            b = (interval_end - left).days // (period * 7)
            total += b - a
        elif left <= interval_end:
            total += (interval_end - left).days // (period * 7) + 1

    return total
