# Placeholder for job.py
# backend/app/schemas/job.py

from pydantic import BaseModel, Field
from typing import Optional, Any

class JobStatus(BaseModel):
    job_id: str
    status: str
    result: Optional[Any] = None