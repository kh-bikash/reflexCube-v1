# backend/app/schemas/base.py

from pydantic import BaseModel

class JobRequest(BaseModel):
    prompt: str