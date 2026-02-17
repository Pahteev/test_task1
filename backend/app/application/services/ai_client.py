import httpx

from app.core.config import settings


class AIClassifierClient:
    async def classify(self, image_url: str) -> dict:
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(settings.ai_service_url, json={"image_url": image_url})
            response.raise_for_status()
            return response.json()
