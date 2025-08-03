import datetime as dt
from enum import Flag, auto
from dataclasses import dataclass
from itertools import dropwhile
import calendar


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
) -> int:
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


@dataclass
class WeeklyRecurringEvent:
    name: str
    start: dt.date
    weekdays: Weekdays
    period: int
    duration: float


def time_taken(
    event: WeeklyRecurringEvent, interval_start: dt.date, interval_end: dt.date
) -> float:
    return count_occurrences(
        event.start, event.weekdays, event.period, interval_start, interval_end
    )


def count_workdays():
    weekday_count = 0
    cal = calendar.Calendar()

    for week in cal.monthdayscalendar(2013, 8):
        for i, day in enumerate(week):
            # not this month's day or a weekend
            if day == 0 or i >= 5:
                continue
            # or some other control if desired...
            weekday_count += 1

    return weekday_count


def count_workdays(current_date: dt.date, month_number: int, year_number: int):
    weekday_count = 0
    cal = calendar.Calendar()

    remaining_dates = dropwhile(
        lambda d: d < current_date,
        cal.itermonthdates(year_number, month_number),
    )
    for date in remaining_dates:
        if date.weekday() < 5:
            weekday_count += 1

    return weekday_count
