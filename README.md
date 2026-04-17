# 📦 Rakuten Product Classification – MLOps Pipeline

![Version](https://img.shields.io/badge/version-v2.0.0-blue)
![Release](https://img.shields.io/github/v/release/DataScientest-Studio/FEV26-CMLOPS-RAKUTEN)
![Python](https://img.shields.io/badge/python-3.10+-yellow)
![Tests](https://img.shields.io/badge/tests-100%25%20passing-brightgreen)

🎯 Objectif  
Classifier automatiquement les produits Rakuten à partir de leur désignation et description, via un pipeline MLOps complet :  
• Entraînement  
• Tracking MLflow  
• Model Registry  
• API FastAPI  
• Tests unitaires / intégration / E2E  

---

## 🏗️ Architecture du Projet

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

Code

---

## 🚀 1. Entraînement du modèle

```bash
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

bash
uvicorn src.api.app:app --reload
Endpoints
GET / → Vérification de disponibilité

POST /predict

Exemple de requête
json
{
  "designation": "chaussure sport",
  "description": "chaussures running homme",
  "run_id": null
}
Header :

Code
x-token: RAKUTEN_SECRET_123
Exemple de réponse
json
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
Tests unitaires :

bash
pytest tests/test_api_unit.py -v
Tests d’intégration :

bash
pytest tests/test_api_integration.py -v
Tests E2E :

bash
pytest tests/test_api_e2e.py -v
100 % des tests passent.

🧱 5. Mode Hybride
run_id = null → modèle Production

run_id = "xxxx" → modèle d’un run spécifique

📈 6. Résultats
• API stable et sécurisée
• Modèle versionné
• Pipeline reproductible
• Tests complets
• Architecture MLOps professionnelle

📦 Versions du Modèle (MLflow Model Registry)
Version	Description	Statut
v1.0.0	Première version stable	Archivée
v2.0.0	Nouvelle architecture MLOps	Active
Production	Modèle utilisé par l’API	✔ En service
Staging	Version en test (optionnel)	🧪 En validation

🔮 7. Améliorations possibles
• Dockerisation
• CI/CD GitHub Actions
• Monitoring
• Déploiement cloud
• Modèle multimodal (texte + image)