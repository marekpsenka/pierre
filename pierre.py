import datetime as dt
from enum import Flag, auto
from dataclasses import dataclass
from itertools import dropwhile
import pandas as pd
import calendar
from typing import Iterable
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


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
    project: str


def time_taken(
    event: WeeklyRecurringEvent, interval_start: dt.date, interval_end: dt.date
) -> float:
    return (
        count_occurrences(
            event.start,
            event.weekdays,
            event.period,
            interval_start,
            interval_end,
        )
        * event.duration
    )


def count_workdays(
    current_date: dt.date, month_number: int, year_number: int
) -> int:
    """Does not take into account public holidays"""
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


def count_workdays_and_calculate_pool(
    year: int, month: int
) -> tuple[float, float]:
    workdays_count = count_workdays(dt.date(year, month, 1), month, year)
    working_time_pool = float(workdays_count * 8)
    return workdays_count, working_time_pool


def calculate_time_taken_by_recurring_events(
    events: Iterable[WeeklyRecurringEvent],
    year: int,
    month: int,
) -> pd.DataFrame:
    _, working_time_pool = count_workdays_and_calculate_pool(year, month)
    last_day = calendar.monthrange(year, month)[1]

    time_taken_df = pd.DataFrame(
        {
            "Name": event.name,
            "Time Taken": time_taken(
                event, dt.date(year, month, 1), dt.date(year, month, last_day)
            ),
        }
        for event in events
    )
    time_taken_df["Pool share"] = time_taken_df["Time Taken"].apply(
        lambda time: time / working_time_pool
    )

    return time_taken_df


def calculate_time_taken_on_projects_by_recurring_events(
    time_taken_by_recurring_events: pd.DataFrame, events: pd.DataFrame
) -> pd.DataFrame:
    time_taken_with_project_data_df = time_taken_by_recurring_events[
        ["Name", "Time Taken"]
    ]
    time_taken_with_project_data_df["Project"] = events["project"]

    time_taken_on_projects_by_recurring_events_df = (
        time_taken_with_project_data_df.groupby("Project").sum()
    ).drop(columns=["Name"])

    return time_taken_on_projects_by_recurring_events_df


def split_unallocated_allocated_time_taken_by_recurring_events(
    project_allocations: dict[str, float], taken_on_projects: pd.DataFrame
) -> tuple[dict[str, float], float]:
    unallocated = 0.0

    allocated: dict[str, float] = dict()
    for row in taken_on_projects.itertuples():
        if row.Index in project_allocations:
            allocated = row._1
        else:
            unallocated += row._1

    return (
        allocated,
        unallocated,
    )


def plot_working_time_pool_breakdown(
    working_time_pool: float,
    project_allocations: dict[str, float],
    time_taken_by_recurring_events_on_allocated_projects: dict[str, float],
    time_taken_by_recurring_events_on_unallocated_projects: float,
) -> tuple[Figure, Axes]:
    unallocated_capacity = 1.0 - sum(project_allocations.values())
    labels = []
    outer = []
    inner = []
    tab20c = plt.color_sequences["tab20c"]
    outer_colors = []
    inner_colors = []
    i = 0
    for key, value in project_allocations.items():
        labels.append(key)
        outer.append(working_time_pool * value)
        outer_colors.append(tab20c[i * 4])
        inner_colors.append(tab20c[i * 4 + 1])
        if key in time_taken_by_recurring_events_on_allocated_projects:
            inner.append(
                working_time_pool * value
                - time_taken_by_recurring_events_on_allocated_projects[key]
            )
            inner.append(
                time_taken_by_recurring_events_on_allocated_projects[key]
            )
            inner_colors.append(tab20c[-1])
        else:
            inner.append(working_time_pool * value)
        i += 1

    labels.append("Unallocated")
    outer.append(unallocated_capacity * working_time_pool)
    outer_colors.append(tab20c[i * 4])
    inner_colors.append(tab20c[i * 4 + 1])
    if time_taken_by_recurring_events_on_unallocated_projects > 0.0:
        inner.append(
            unallocated_capacity * working_time_pool
            - time_taken_by_recurring_events_on_unallocated_projects
        )
        inner.append(time_taken_by_recurring_events_on_unallocated_projects)
        inner_colors.append(tab20c[-1])
    else:
        inner.append(unallocated_capacity * working_time_pool)

    fig, ax = plt.subplots()

    size = 0.3

    ax.pie(
        outer,
        radius=1,
        colors=outer_colors,
        wedgeprops=dict(width=size, edgecolor="w"),
        labels=labels,
    )

    ax.pie(
        inner,
        radius=1 - size,
        autopct="%1.1f%%",
        colors=inner_colors,
        wedgeprops=dict(width=size, edgecolor="w"),
    )

    ax.set(aspect="equal", title="Working time pool breakdown")

    return fig, ax
