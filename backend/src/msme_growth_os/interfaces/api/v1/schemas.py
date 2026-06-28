from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str


class RecommendationRequestResponse(BaseModel):
    business_id: str
    status: str
    message: str
