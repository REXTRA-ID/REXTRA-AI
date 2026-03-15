from pydantic import BaseModel, ConfigDict
from datetime import datetime
from uuid import UUID
from app.api.v1.general.schemas.catogory import CategoryResponse


class HistoryResponse(BaseModel):
    id: int
    user_id: UUID          # FIX: harusnya UUID bukan int
    test_category: CategoryResponse
    status: str
    started_at: datetime
    completed_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
