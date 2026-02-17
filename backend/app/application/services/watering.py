from datetime import date, timedelta


def calculate_next_watering(last_watering_date: date | None, water_interval_days: int) -> date | None:
    if not last_watering_date:
        return None
    return last_watering_date + timedelta(days=water_interval_days)
