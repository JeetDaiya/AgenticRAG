from pydantic import BaseModel, Field


class PlannerResponse(BaseModel):
    should_proceed : bool = Field(default_factory=False, description='A boolean which will decide if we will proceed to retrieve document or not.')
        
    