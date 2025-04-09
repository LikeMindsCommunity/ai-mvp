from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class GenerateCodeRequest(BaseModel):
    prompt: str
    project_id: Optional[str] = None

class GenerateCodeResponse(BaseModel):
    success: bool
    code: Optional[str] = None
    project_id: str
    errors: Optional[List[str]] = None

class WebSocketMessage(BaseModel):
    type: str  # status|error|preview|completion
    data: Dict[str, Any]
    timestamp: datetime

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 