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
