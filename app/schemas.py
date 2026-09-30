from enum import Enum
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl

class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    OPTIONS = "OPTIONS"

class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"

class SimulationRequest(BaseModel):
    request_origin: str = Field(..., example="https://app.example.com")
    target_url: str = Field(..., example="https://api.example.com/v1/data")
    request_method: HttpMethod = Field(..., example="POST")
    request_headers: List[str] = Field(default=[], example=["Content-Type", "Authorization"])
    with_credentials: bool = Field(default=False)
    server_config_raw: Optional[str] = Field(default=None, description="Raw web server or gateway config content")

class SecurityFinding(BaseModel):
    id: str
    severity: Severity
    title: str
    description: str
    rule_violated: str

class AnalysisResponse(BaseModel):
    is_allowed: bool
    status_code: int
    explanation: str
    matched_rules: Dict[str, str]
    findings: List[SecurityFinding]
    safe_snippets: Dict[str, str]