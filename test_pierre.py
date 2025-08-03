import pierre
import datetime as dt


def test_1():
    month_start = dt.date(2025, 8, 1)
    month_end = dt.date(2025, 8, 31)

    start = dt.date(2025, 7, 23)
    period = 1

    weekdays = pierre.Weekdays.MON | pierre.Weekdays.WED | pierre.Weekdays.FRI

    assert (
        pierre.count_occurrences(
            start, weekdays, period, month_start, month_end
        )
        == 13
    )


def test_2():
    interval_start = dt.date(2025, 7, 31)
    interval_end = dt.date(2025, 8, 7)

    start = dt.date(2025, 7, 30)
    period = 1
    weekdays = pierre.Weekdays.TUE | pierre.Weekdays.THU
    assert (
        pierre.count_occurrences(
            start, weekdays, period, interval_start, interval_end
        )
        == 3
    )


def test_3():
    interval_start = dt.date(2025, 8, 13)
    interval_end = dt.date(2025, 8, 14)

    start = dt.date(2025, 8, 1)
    period = 1
    weekdays = pierre.Weekdays.MON | pierre.Weekdays.FRI
    assert (
        pierre.count_occurrences(
            start, weekdays, period, interval_start, interval_end
        )
        == 0
    )


def test_4():
    interval_start = dt.date(2025, 8, 13)
    interval_end = dt.date(2025, 8, 14)

    start = dt.date(2025, 8, 15)
    period = 1
    weekdays = pierre.Weekdays.WED | pierre.Weekdays.THU
    assert (
        pierre.count_occurrences(
            start, weekdays, period, interval_start, interval_end
        )
        == 0
    )


def test_5():
    interval_start = dt.date(2025, 8, 11)
    interval_end = dt.date(2025, 8, 15)

    start = dt.date(2025, 8, 11)
    period = 1
    weekdays = pierre.Weekdays.MON | pierre.Weekdays.WED | pierre.Weekdays.THU
    assert (
        pierre.count_occurrences(
            start, weekdays, period, interval_start, interval_end
        )
        == 3
    )
