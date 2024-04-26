from datetime import datetime
from pydantic import BaseModel


class BaseCommon(BaseModel):
    id: int
    created_at: datetime
