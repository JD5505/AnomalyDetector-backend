from pydantic import BaseModel, Field
from datetime import datetime

class LocationSample(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime


class LocationSequence(BaseModel):
    samples: list[LocationSample] = Field(min_length=31, max_length=31)