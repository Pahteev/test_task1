from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.db.base import AuditMixin, Base


class User(Base, AuditMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    locale: Mapped[str] = mapped_column(String(5), default="ru")


class Plant(Base, AuditMixin):
    __tablename__ = "plants"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    latin_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    light_requirements: Mapped[str | None] = mapped_column(String(255), nullable=True)
    care_recommendations: Mapped[str | None] = mapped_column(Text, nullable=True)
    water_interval_days: Mapped[int] = mapped_column(Integer, default=7)
    last_watering_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    next_watering_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)


class PlantImage(Base, AuditMixin):
    __tablename__ = "plant_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id", ondelete="CASCADE"), index=True)
    image_url: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(32), default="uploaded")


class WaterLog(Base, AuditMixin):
    __tablename__ = "water_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id", ondelete="CASCADE"), index=True)
    watered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class AISuggestion(Base, AuditMixin):
    __tablename__ = "ai_suggestions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plant_image_id: Mapped[int] = mapped_column(ForeignKey("plant_images.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(255))
    latin_name: Mapped[str] = mapped_column(String(255))
    water_interval_days: Mapped[int] = mapped_column(Integer)
    light_requirements: Mapped[str] = mapped_column(String(255))
    care_recommendations: Mapped[str] = mapped_column(Text)
    accepted: Mapped[bool] = mapped_column(Boolean, default=False)


class TelegramSetting(Base, AuditMixin):
    __tablename__ = "telegram_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    chat_id_encrypted: Mapped[str] = mapped_column(String(500))
    notifications_enabled: Mapped[bool] = mapped_column(Boolean, default=True)


class Notification(Base, AuditMixin):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    plant_id: Mapped[int] = mapped_column(ForeignKey("plants.id", ondelete="CASCADE"), index=True)
    channel: Mapped[str] = mapped_column(String(32), default="telegram")
    message: Mapped[str] = mapped_column(Text)
    sent_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


Index("ix_notifications_user_sent", Notification.user_id, Notification.sent_at)
