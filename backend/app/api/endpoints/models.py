# Placeholder for models.py
# backend/app/api/endpoints/models.py

from fastapi import APIRouter

router = APIRouter()

# Placeholder endpoint for fetching model info
@router.get("/{model_id}")
def get_model_details(model_id: str):
    return {"model_id": model_id, "message": "Model details endpoint is not yet implemented."}