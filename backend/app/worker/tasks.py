import time
import os
import mlflow
from app.worker.celery_app import celery_app
from app.scripts.data_ingestion.newsapi_connector import fetch_real_news_data
from app.scripts.model_training.train_lora import train_real_lora_model

def parse_prompt(prompt: str) -> dict:
    print(f"Parsing prompt: '{prompt}'")
    if "news" in prompt.lower() and "finance" in prompt.lower():
        return {"topic": "finance", "source": "newsapi"}
    return {"topic": "machine learning", "source": "newsapi"}

def get_or_create_experiment(experiment_name: str):
    client = mlflow.tracking.MlflowClient()
    experiment = client.get_experiment_by_name(experiment_name)
    if experiment is None:
        print(f"Experiment '{experiment_name}' not found. Creating a new one.")
        experiment_id = client.create_experiment(experiment_name)
        return experiment_id
    return experiment.experiment_id

@celery_app.task(bind=True, name="app.worker.tasks.run_training_pipeline")
def run_training_pipeline(self, prompt: str):
    mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI"))
    
    experiment_name = "AutoModeler_Runs"
    get_or_create_experiment(experiment_name)
    mlflow.set_experiment(experiment_name)

    with mlflow.start_run() as run:
        run_id = run.info.run_id
        mlflow.log_param("prompt", prompt)
        print(f"✅ Starting pipeline for run_id: {run_id}")

        try:
            self.update_state(state='PROGRESS', meta={'step': 1, 'status': 'Parsing prompt'})
            params = parse_prompt(prompt)
            mlflow.log_param("topic", params['topic'])

            self.update_state(state='PROGRESS', meta={'step': 2, 'status': 'Gathering data'})
            raw_data_path = fetch_real_news_data(params['topic'], "data/raw")
            if not raw_data_path:
                raise Exception("Data fetching failed and returned no path.")
            print(f"✅ Data gathering complete. Path: {raw_data_path}")
            
            self.update_state(state='PROGRESS', meta={'step': 3, 'status': 'Versioning data'})
            os.system(f"dvc add {raw_data_path}")
            print(f"✅ Data versioned with DVC.")
            
            self.update_state(state='PROGRESS', meta={'step': 4, 'status': 'Training model'})
            model_output_dir = train_real_lora_model(
                data_path=raw_data_path,
                base_model="distilbert-base-uncased",
                run_id=run_id
            )
            mlflow.log_artifacts(model_output_dir, artifact_path="model")
            print(f"✅ Model training complete.")
            
            final_result = { "status": "SUCCESS", "run_id": run_id }
            return final_result

        except Exception as e:
            error_message = f"Error in pipeline for run {run_id}: {e}"
            print(f"❌ {error_message}")
            mlflow.set_tag("status", "failed")
            # This updated line fixes the Celery error reporting
            self.update_state(state='FAILURE', meta={'exc_type': type(e).__name__, 'exc_message': str(e)})
            return {"status": "FAILURE", "error": str(e)}