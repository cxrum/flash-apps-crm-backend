from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FlexibleCommand(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)
    success: bool = True


class PaginationCommand(FlexibleCommand):
    limit: int | None = Field(default=None, ge=1, le=1000)
    offset: int | None = Field(default=None, ge=0)
    search: str | None = None
    start_at: datetime | None = None
    end_at: datetime | None = None


JsonDict = dict[str, Any]

class BaseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, frozen=True)
    
class TimeMarked(BaseModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None