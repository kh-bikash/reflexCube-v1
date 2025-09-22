# backend/app/api/endpoints/jobs.py

from fastapi import APIRouter, HTTPException
from celery import Celery
from celery.result import AsyncResult
from app.schemas.base import JobRequest
from app.schemas.job import JobStatus

# Create a new, separate Celery instance for the API to use as a client.
# It connects to the same Redis broker as the worker.
api_celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

router = APIRouter()

@router.post("/request-model", response_model=JobStatus, status_code=202)
def request_model(job_request: JobRequest):
    """
    Accepts a natural language prompt to start a model training job.
    """
    # Send the task by its full, registered string name.
    task = api_celery_app.send_task("app.worker.tasks.run_training_pipeline", args=[job_request.prompt])
    return JobStatus(job_id=task.id, status="PENDING")


@router.get("/status/{job_id}", response_model=JobStatus)
def get_status(job_id: str):
    """
    Retrieves the status of a background job.
    """
    # Use the same app instance to fetch the result.
    task_result = AsyncResult(job_id, app=api_celery_app)
    status = task_result.status
    result = task_result.result

    if status == "FAILURE":
        print(f"Job {job_id} failed. Reason: {result}")
        raise HTTPException(status_code=500, detail=f"Job failed: {str(result)}")

    return JobStatus(job_id=job_id, status=status, result=result)