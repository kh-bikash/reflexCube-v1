# Reflex Cube: AI Model Generation Platform

Reflex Cube is a full-stack MLOps platform that automatically gathers data, trains a model, and serves it based on a natural language prompt.

## Architecture
- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (TypeScript)
- **Background Jobs**: Celery with Redis
- **Data Versioning**: DVC
- **Experiment Tracking**: MLflow
- **Containerization**: Docker
- **Cloud Infrastructure**: Google Cloud (Cloud Run, Vertex AI, GCS)
- **Infrastructure as Code**: Terraform

## Local Development Setup (VS Code + WSL)

### Prerequisites
1.  **Docker Desktop**: Install on Windows and ensure it's integrated with WSL2.
2.  **WSL2**: Make sure you have a Linux distribution (e.g., Ubuntu) installed.
3.  **VS Code**: with the "Remote - Containers" extension.
4.  **Google Cloud SDK**: `gcloud` CLI installed and authenticated (`gcloud auth application-default login`).
5.  **Git**: For version control.

### Quickstart
1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd automodeler
    ```

2.  **Set up Environment Variables**:
    - Copy `backend/.env.example` to `backend/.env`.
    - Fill in the values:
      - `NEWS_API_KEY`: Get from [NewsAPI.org](https://newsapi.org/).
      - `MLFLOW_TRACKING_URI`: Set to `http://mlflow:5001`.
      - `GOOGLE_APPLICATION_CREDENTIALS`: If running locally and not in a container with gcloud auth, you might need this.
      - `GCP_PROJECT_ID`: Your Google Cloud project ID.
      - `GCP_REGION`: e.g., `us-central1`.
      - `GCS_BUCKET_NAME`: A unique GCS bucket name for DVC remote storage.

3.  **Launch the Dev Container**:
    - Open the `automodeler` folder in VS Code.
    - VS Code will prompt: "Reopen in Container". Click it.
    - This will build and launch the `docker-compose` stack. The terminal will be inside the `backend` container.

4.  **Initialize DVC**:
    - In the VS Code terminal (inside the dev container):
    ```bash
    # Initialize DVC
    dvc init

    # Configure remote storage (replace with your bucket name)
    dvc remote add -d gcs gcs://${GCS_BUCKET_NAME}/dvc

    # (Optional) Log in to GCP if needed
    gcloud auth application-default login
    ```

5.  **Run the application**:
    The dev container should have already started the services.
    - **Backend**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **Frontend**: [http://localhost:3000](http://localhost:3000)
    - **MLflow**: [http://localhost:5001](http://localhost:5001)

### Running the Smoke Test
From the VS Code terminal inside the dev container:
```bash
pytest tests/e2e/test_smoke.py

#### `LEGAL.md`
Outlines data usage policies and compliance measures.

```markdown
# AutoModeler: Legal & Compliance

This document outlines the legal and ethical considerations for data usage within the AutoModeler platform.

## Data Provenance and Licensing
- **Principle**: We only use data from sources with clear licensing terms that permit this type of use.
- **Metadata**: Every piece of data used for training is stored with provenance metadata, including `source_url`, `license_type`, `retrieval_timestamp`, and a link to the source's Terms of Service.
- **Model Cards**: Every model generated includes a "Data" section in its Model Card, listing the datasets used and their licenses.

## Web Scraping Policy
- **Robots.txt**: Our `html_scraper.py` module programmatically checks and **strictly adheres** to the `robots.txt` file of any domain before fetching data. If crawling is disallowed for our user-agent (`AutoModelerBot/1.0`), the scraper will not proceed.
- **Rate Limiting**: All scraping activities are rate-limited to avoid overwhelming source servers. The default is a 2-second delay between requests to the same domain.
- **Opt-Out**: We provide a clear contact method (`legal@automodeler.example.com`) for data source owners to request that their site not be used. We maintain a central exclusion list.

## Personally Identifiable Information (PII)
- **Avoidance**: Data ingestion scripts are designed to target non-personal, public information (e.g., news articles, public records).
- **Anonymization**: We will implement PII detection and redaction steps during data preprocessing for unstructured text sources where accidental PII inclusion is possible.
- **User Data**: User-provided data is subject to our Privacy Policy and is not used for training public models without explicit consent.

## Checklist for Ethical & Compliant Data Usage
- [X] Does the data source have a clear license (e.g., Creative Commons, MIT, Apache)?
- [X] Have we stored the license and source URL with the data?
- [X] If scraping, have we checked and honored `robots.txt`?
- [X] Is our scraper rate-limited and does it use a transparent user-agent?
- [X] Have we made a reasonable effort to avoid collecting PII?
- [X] Is the data provenance clearly documented in the final Model Card?
- [X] Is there a clear opt-out path for data source owners?
