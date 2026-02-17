from datetime import date

from app.application.services.watering import calculate_next_watering


def test_calculate_next_watering() -> None:
    assert calculate_next_watering(date(2026, 1, 1), 5) == date(2026, 1, 6)


def test_calculate_next_watering_with_none() -> None:
    assert calculate_next_watering(None, 5) is None
