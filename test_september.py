from pierre import Weekdays, count_occurrences, count_workdays
import datetime as dt


def test_1():
    interval_start = dt.date(2025, 8, 1)
    interval_end = dt.date(2025, 9, 30)

    start = dt.date(2025, 6, 18)
    end = dt.date(2025, 9, 12)
    period = 1

    weekdays = (
        Weekdays.MON
        | Weekdays.TUE
        | Weekdays.WED
        | Weekdays.THU
        | Weekdays.FRI
    )

    assert (
        count_occurrences(
            start, end, weekdays, period, interval_start, interval_end
        )
        == 31
    )


def test_2():
    interval_start = dt.date(2025, 8, 1)
    interval_end = dt.date(2025, 9, 30)

    start = dt.date(2025, 7, 23)
    end = dt.date(2025, 8, 31)
    period = 1

    weekdays = Weekdays.MON | Weekdays.WED | Weekdays.FRI

    assert (
        count_occurrences(
            start, end, weekdays, period, interval_start, interval_end
        )
        == 13
    )


def test_3():
    interval_start = dt.date(2025, 8, 1)
    interval_end = dt.date(2025, 9, 30)

    start = dt.date(2025, 8, 4)
    end = dt.date(2025, 8, 27)
    period = 1

    weekdays = Weekdays.MON | Weekdays.WED | Weekdays.FRI

    assert (
        count_occurrences(
            start, end, weekdays, period, interval_start, interval_end
        )
        == 11
    )


def test_4():
    interval_start = dt.date(2025, 8, 1)
    interval_end = dt.date(2025, 9, 30)

    start = dt.date(2025, 7, 31)
    end = dt.date(2025, 12, 31)
    period = 2

    weekdays = Weekdays.THU

    assert (
        count_occurrences(
            start, end, weekdays, period, interval_start, interval_end
        )
        == 4
    )


def test_5():
    interval_start = dt.date(2025, 8, 1)
    interval_end = dt.date(2025, 9, 30)

    start = dt.date(2025, 8, 14)
    period = 2

    weekdays = Weekdays.THU

    assert (
        count_occurrences(
            start, None, weekdays, period, interval_start, interval_end
        )
        == 4
    )


def test_6():
    interval_start = dt.date(2025, 8, 1)
    interval_end = dt.date(2025, 9, 30)

    start = dt.date(2025, 7, 25)
    period = 4

    weekdays = Weekdays.FRI

    assert (
        count_occurrences(
            start, None, weekdays, period, interval_start, interval_end
        )
        == 2
    )


def test_7():
    interval_start = dt.date(2025, 8, 1)
    interval_end = dt.date(2025, 9, 30)

    start = dt.date(2025, 7, 21)
    end = dt.date(2025, 11, 1)
    period = 2

    weekdays = Weekdays.MON

    assert (
        count_occurrences(
            start, end, weekdays, period, interval_start, interval_end
        )
        == 5
    )


def test_8():
    interval_start = dt.date(2025, 8, 1)
    interval_end = dt.date(2025, 9, 30)

    start = dt.date(2025, 7, 18)
    end = dt.date(2025, 10, 30)
    period = 2

    weekdays = Weekdays.FRI

    assert (
        count_occurrences(
            start, end, weekdays, period, interval_start, interval_end
        )
        == 5
    )


def test_workdays_in_september_are_counted_correctly():
    current_date = dt.date(2025, 9, 1)
    assert count_workdays(current_date, 9, 2025) == 22


def test_remaining_september_in_august_are_counted_correctly():
    current_date = dt.date(2025, 9, 3)
    assert count_workdays(current_date, 9, 2025) == 20
