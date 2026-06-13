from __future__ import annotations
import copy
from datetime import datetime, tzinfo
from typing import TypeVar
import pytz
from pydantic import BaseModel, ConfigDict, Field

class TransportPayload(BaseModel):
    model_config = ConfigDict(extra="allow", populate_by_name=True)


class PaginationQueryPayload(TransportPayload):
    limit: int | None = Field(default=None, ge=1, le=1000)
    offset: int | None = Field(default=None, ge=0)
    search: str | None = None
    start_at: datetime | None = None # date time ISO 8601 Local with Offset
    end_at: datetime | None = None # date time ISO 8601 Local with Offset