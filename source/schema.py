from typing import Optional

from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=1,
        description="User query"
    )


class QueryResponse(BaseModel):
    status: str
    response: str


class HealthResponse(BaseModel):
    status: str


class AgentInfoResponse(BaseModel):
    agent_name: str
    model: str
    vector_store: str
    database: str
    status: str


class ErrorResponse(BaseModel):
    status: str
    message: str
    details: Optional[str] = None