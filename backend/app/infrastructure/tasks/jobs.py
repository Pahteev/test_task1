from datetime import date

from sqlalchemy import select

from app.infrastructure.db.models import Notification, Plant
from app.infrastructure.db.session import SessionLocal
from app.infrastructure.tasks.celery_app import celery_app


@celery_app.task
def check_watering_schedule() -> int:
    import asyncio

    async def _inner() -> int:
        async with SessionLocal() as session:
            result = await session.execute(
                select(Plant).where(Plant.next_watering_date <= date.today(), Plant.deleted_at.is_(None))
            )
            due_plants = result.scalars().all()
            for plant in due_plants:
                session.add(Notification(user_id=plant.user_id, plant_id=plant.id, message=f"Time to water {plant.name}"))
            await session.commit()
            return len(due_plants)

    return asyncio.run(_inner())
