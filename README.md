# 🤖 Reflex Cube – AI Model Generation Platform  

> *“Reflex Cube is an intelligent AI agent platform that handles everything—from model training to testing—locally, providing instant results and downloadable models.”*  

---

![Reflex Cube Banner](https://img.shields.io/badge/Reflex%20Cube-AI%20Platform-blueviolet?style=for-the-badge&logo=tensorflow) ![FastAPI](https://img.shields.io/badge/FastAPI-Backend-brightgreen?style=for-the-badge&logo=fastapi) ![Next.js](https://img.shields.io/badge/Next.js-Frontend-black?style=for-the-badge&logo=next.js) ![Celery](https://img.shields.io/badge/Celery-Task%20Queue-lightgrey?style=for-the-badge&logo=celery) ![Redis](https://img.shields.io/badge/Redis-Queue-red?style=for-the-badge&logo=redis) ![MLflow](https://img.shields.io/badge/MLflow-Tracking-orange?style=for-the-badge&logo=mlflow)  


  


---

## ✨ Features

- 🎯 **Prompt-Based AI Model Generation** – Generate models automatically by providing a prompt.  
- ⚡ **Local Training with LoRA** – Efficiently train AI models on your local machine.  
- 🛠️ **Automated Task Management** – Redis + Celery handle background tasks seamlessly.  
- 📊 **Experiment Tracking** – Monitor metrics, hyperparameters, and logs using MLflow.  
- 💾 **Local Model Storage & Registry** – Manage trained models locally with versioning.  
- 🌐 **Interactive Dashboard** – Test, monitor, and download models via an intuitive interface.  
- 🎨 **Animated Progress** – Visualize training and evaluation with real-time animations.  

---

## 🛠️ Tech Stack

| Layer               | Technology |
|--------------------|------------|
| Frontend           | Next.js (React) |
| Backend            | FastAPI |
| Task Queue         | Redis |
| Worker             | Celery |
| Model Training     | LoRA (Local) |
| Experiment Tracking| MLflow |
| Storage            | Local filesystem / MLflow registry |

---

## ⚡ Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/reflexcube/reflex-cube.git
cd reflex-cube
