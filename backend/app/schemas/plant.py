from datetime import date, datetime

from pydantic import BaseModel, Field


class PlantCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    latin_name: str | None = None
    water_interval_days: int = Field(default=7, ge=1, le=60)
    last_watering_date: date | None = None


class PlantOut(BaseModel):
    id: int
    name: str
    latin_name: str | None
    water_interval_days: int
    last_watering_date: date | None
    next_watering_date: date | None


class WaterLogRequest(BaseModel):
    watered_at: datetime


class PlantImageRequest(BaseModel):
    image_url: str
