# Placeholder for jobs.py
from fastapi import APIRouter, HTTPException
from celery.result import AsyncResult
from worker.celery_app import celery_app
from app.schemas.job import JobRequest, JobStatus

router = APIRouter()

@router.post("/request-model", response_model=JobStatus, status_code=202)
def request_model(job_request: JobRequest):
    """
    Accepts a natural language prompt to start a model training job.
    """
    task = celery_app.send_task("worker.tasks.run_training_pipeline", args=[job_request.prompt])
    return JobStatus(job_id=task.id, status="PENDING")


@router.get("/status/{job_id}", response_model=JobStatus)
def get_status(job_id: str):
    """
    Retrieves the status of a background job.
    """
    task_result = AsyncResult(job_id, app=celery_app)
    status = task_result.status
    result = task_result.result

    if status == "FAILURE":
        # Log the error properly in a real app
        print(f"Job {job_id} failed. Reason: {result}")
        raise HTTPException(status_code=500, detail=f"Job failed: {str(result)}")

    return JobStatus(job_id=job_id, status=status, result=result)