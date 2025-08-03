from pierre import Weekdays, count_occurrences, count_workdays
import datetime as dt


def test_1():
    month_start = dt.date(2025, 8, 1)
    month_end = dt.date(2025, 8, 31)

    start = dt.date(2025, 6, 18)
    period = 1

    weekdays = (
        Weekdays.MON
        | Weekdays.TUE
        | Weekdays.WED
        | Weekdays.THU
        | Weekdays.FRI
    )

    assert (
        count_occurrences(start, weekdays, period, month_start, month_end)
        == 21
    )


def test_2():
    month_start = dt.date(2025, 8, 1)
    month_end = dt.date(2025, 8, 31)

    start = dt.date(2025, 7, 23)
    period = 1

    weekdays = Weekdays.MON | Weekdays.WED | Weekdays.FRI

    assert (
        count_occurrences(start, weekdays, period, month_start, month_end)
        == 13
    )


def test_3():
    month_start = dt.date(2025, 8, 1)
    month_end = dt.date(2025, 8, 31)

    start = dt.date(2025, 8, 4)
    period = 1

    weekdays = Weekdays.MON | Weekdays.WED | Weekdays.FRI

    assert (
        count_occurrences(start, weekdays, period, month_start, month_end)
        == 12
    )


def test_4():
    month_start = dt.date(2025, 8, 1)
    month_end = dt.date(2025, 8, 31)

    start = dt.date(2025, 7, 31)
    period = 2

    weekdays = Weekdays.THU

    assert (
        count_occurrences(start, weekdays, period, month_start, month_end) == 2
    )


def test_5():
    month_start = dt.date(2025, 8, 1)
    month_end = dt.date(2025, 8, 31)

    start = dt.date(2025, 8, 14)
    period = 2

    weekdays = Weekdays.THU

    assert (
        count_occurrences(start, weekdays, period, month_start, month_end) == 2
    )


def test_6():
    month_start = dt.date(2025, 8, 1)
    month_end = dt.date(2025, 8, 31)

    start = dt.date(2025, 7, 25)
    period = 4

    weekdays = Weekdays.FRI

    assert (
        count_occurrences(start, weekdays, period, month_start, month_end) == 1
    )


def test_7():
    month_start = dt.date(2025, 8, 1)
    month_end = dt.date(2025, 8, 31)

    start = dt.date(2025, 7, 21)
    period = 2

    weekdays = Weekdays.MON

    assert (
        count_occurrences(start, weekdays, period, month_start, month_end) == 2
    )


def test_8():
    month_start = dt.date(2025, 8, 1)
    month_end = dt.date(2025, 8, 31)

    start = dt.date(2025, 7, 18)
    period = 2

    weekdays = Weekdays.FRI

    assert (
        count_occurrences(start, weekdays, period, month_start, month_end) == 3
    )


def test_workdays_in_august_are_counted_correctly():
    current_date = dt.date(2025, 8, 1)
    assert count_workdays(current_date, 8, 2025) == 21


def test_remaining_workdays_in_august_are_counted_correctly():
    current_date = dt.date(2025, 8, 3)
    assert count_workdays(current_date, 8, 2025) == 20
