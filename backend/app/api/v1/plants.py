from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.application.services.ai_client import AIClassifierClient
from app.application.services.watering import calculate_next_watering
from app.infrastructure.db.models import AISuggestion, Plant, PlantImage, User, WaterLog
from app.infrastructure.db.session import get_db_session
from app.schemas.plant import PlantCreate, PlantImageRequest, PlantOut, WaterLogRequest

router = APIRouter(prefix="/plants", tags=["plants"])




@router.get("", response_model=list[PlantOut])
async def list_plants(
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> list[PlantOut]:
    result = await db.execute(select(Plant).where(Plant.user_id == user.id, Plant.deleted_at.is_(None)))
    plants = result.scalars().all()
    return [PlantOut.model_validate(p, from_attributes=True) for p in plants]

@router.post("", response_model=PlantOut)
async def create_plant(
    payload: PlantCreate,
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> PlantOut:
    next_watering = calculate_next_watering(payload.last_watering_date, payload.water_interval_days)
    plant = Plant(
        user_id=user.id,
        name=payload.name,
        latin_name=payload.latin_name,
        water_interval_days=payload.water_interval_days,
        last_watering_date=payload.last_watering_date,
        next_watering_date=next_watering,
    )
    db.add(plant)
    await db.commit()
    await db.refresh(plant)
    return PlantOut.model_validate(plant, from_attributes=True)


@router.post("/{plant_id}/water", response_model=PlantOut)
async def report_watering(
    plant_id: int,
    payload: WaterLogRequest,
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> PlantOut:
    result = await db.execute(select(Plant).where(Plant.id == plant_id, Plant.user_id == user.id, Plant.deleted_at.is_(None)))
    plant = result.scalar_one_or_none()
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")

    plant.last_watering_date = payload.watered_at.date()
    plant.next_watering_date = calculate_next_watering(plant.last_watering_date, plant.water_interval_days)
    db.add(WaterLog(plant_id=plant.id, watered_at=payload.watered_at))
    await db.commit()
    await db.refresh(plant)
    return PlantOut.model_validate(plant, from_attributes=True)


@router.post("/{plant_id}/images/classify")
async def classify_plant_image(
    plant_id: int,
    payload: PlantImageRequest,
    db: AsyncSession = Depends(get_db_session),
    user: User = Depends(get_current_user),
) -> dict:
    result = await db.execute(select(Plant).where(Plant.id == plant_id, Plant.user_id == user.id, Plant.deleted_at.is_(None)))
    plant = result.scalar_one_or_none()
    if not plant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plant not found")

    image = PlantImage(plant_id=plant.id, image_url=payload.image_url, status="processing")
    db.add(image)
    await db.commit()
    await db.refresh(image)

    ai_payload = await AIClassifierClient().classify(payload.image_url)
    suggestion = AISuggestion(
        plant_image_id=image.id,
        name=ai_payload["name"],
        latin_name=ai_payload["latin_name"],
        water_interval_days=ai_payload["water_interval_days"],
        light_requirements=ai_payload["light_requirements"],
        care_recommendations=ai_payload["care_recommendations"],
    )
    image.status = "classified"
    await db.merge(suggestion)
    await db.commit()

    return {
        "image_id": image.id,
        "suggestion": {
            "name": suggestion.name,
            "latin_name": suggestion.latin_name,
            "water_interval_days": suggestion.water_interval_days,
            "light_requirements": suggestion.light_requirements,
            "care_recommendations": suggestion.care_recommendations,
            "classified_at": datetime.utcnow().isoformat(),
        },
    }
