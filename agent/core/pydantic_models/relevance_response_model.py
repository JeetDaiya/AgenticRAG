from pydantic import BaseModel, Field
from enum import StrEnum

class Choice(StrEnum):
    YES = "yes"
    NO = "no"

class RelevanceResponse(BaseModel):
    choice : Choice = Field("a yes or no field which tells about relevance of retrieved chunks")