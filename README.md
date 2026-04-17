📦 Rakuten Product Classification – MLOps Pipeline
🎯 Objectif
Classifier automatiquement les produits Rakuten à partir de leur désignation et description, via un pipeline MLOps complet :
    • Entraînement 
    • Tracking MLflow 
    • Model Registry 
    • API FastAPI 
    • Tests unitaires / intégration / E2E 

🏗️ Architecture du Projet
project/
│
├── src/
│   ├── data/
│   ├── models/
│   ├── api/
│   │   ├── app.py
│   │   ├── prediction_service.py
│   │   ├── utils.py
│   │   └── schemas.py
│   ├── utils/
│   ├── models/
│   └── train.py
│
├── mlflow.db
├── tests/
├── README.md
└── requirements.txt

🚀 1. Entraînement du modèle
python src/train.py --mode full
MLflow logge :
    • paramètres 
    • métriques 
    • artefacts 
    • modèle sklearn 
    • version dans le Model Registry 

📚 2. MLflow Model Registry
Le modèle est enregistré sous :
rakuten_classifier
Avec versions :
    • v1, v2, v3… 
    • Production = version utilisée par l’API 

🌐 3. API FastAPI
Lancer l’API :
uvicorn src.api.app:app --reload
Endpoints
GET /
→ Vérification de disponibilité
POST /predict
Body :
{
  "designation": "chaussure sport",
  "description": "chaussures running homme",
  "run_id": null
}
Header :
x-token: RAKUTEN_SECRET_123
Réponse :
{
  "prediction_code": 21,
  "label": "Fournitures Papeterie",
  "run_id": null,
  "confidence": null,
  "inference_time_ms": 12.4,
  "model_uuid": "unknown",
  "model_version": "Production",
  "timestamp": "2026-04-17T08:12:45Z"
}

🧪 4. Tests Automatisés
Tests unitaires
pytest tests/test_api_unit.py -v
Tests d’intégration
pytest tests/test_api_integration.py -v
Tests E2E
pytest tests/test_api_e2e.py -v
100 % des tests passent.

🧱 5. Mode Hybride
    • run_id = null → modèle Production 
    • run_id = "xxxx" → modèle d’un run spécifique 

📈 6. Résultats
    • API stable et sécurisée 
    • Modèle versionné 
    • Pipeline reproductible 
    • Tests complets 
    • Architecture MLOps professionnelle 

🔮 7. Améliorations possibles
    • Dockerisation 
    • CI/CD GitHub Actions 
    • Monitoring 
    • Déploiement cloud 
    • Modèle multimodal (texte + image) 

