Architecture complète — Version 2 du projet MLOps Rakuten

Vue d’ensemble, schémas, explications techniques et MLOps

🟦 1. Introduction
Ce document présente l’architecture complète de la Version 2 du projet Rakuten Classification.
Il explique :

l’architecture logicielle

l’architecture MLOps

l’architecture API

l’architecture MLflow

les flux de données

les interactions entre composants

Il est destiné :

à l’équipe débutante

au jury

aux nouveaux contributeurs

à toute personne souhaitant comprendre le fonctionnement interne du projet

🟩 2. Architecture globale du projet
Voici la structure générale du projet :

Code
FEV26-CMLOPS-RAKUTEN/
│
├── src/
│   ├── api/
│   │   ├── app.py
│   │   ├── prediction_service.py
│   │   ├── utils.py
│   │   └── schemas.py
│   │
│   ├── models/
│   │   └── train.py
│   │
│   └── utils/
│
├── tests/
├── mlruns/
├── mlflow.db
├── README.md
└── docs/
Rôle de chaque dossier
Dossier	Rôle
src/api/	API FastAPI + logique de prédiction
src/models/	Entraînement du modèle
src/utils/	Fonctions utilitaires
tests/	Tests unitaires, intégration, E2E
mlruns/	Artefacts MLflow
mlflow.db	Base SQLite MLflow
docs/	Documentation pédagogique

🟦 3. Architecture MLOps (vue d’ensemble)
Voici la vue macro du pipeline MLOps :

Code
          ┌────────────────────────┐
          │      Données brutes    │
          └─────────────┬──────────┘
                        │
                        ▼
              Préprocessing texte
                        │
                        ▼
               Pipeline sklearn
                        │
                        ▼
               Entraînement modèle
                        │
                        ▼
                 MLflow Tracking
                        │
                        ▼
                Model Registry MLflow
                        │
                        ▼
                API FastAPI /predict
                        │
                        ▼
                Réponse JSON enrichie
🟧 4. Architecture API (FastAPI)
L’API est composée de 4 fichiers principaux :

Code
src/api/
│
├── app.py                ← Définition des endpoints
├── prediction_service.py ← Logique métier de prédiction
├── utils.py              ← Chargement modèle MLflow
└── schemas.py            ← Validation Pydantic
Schéma API
Code
Client
  │
  ├── POST /predict
  │       │
  │       ▼
  │   Validation Pydantic (schemas.py)
  │       │
  │       ▼
  │   prediction_service.py
  │       │
  │       ▼
  │   utils.load_model() (MLflow)
  │       │
  │       ▼
  │   modèle.predict()
  │       │
  │       ▼
  │   mapping code → label
  │       │
  │       ▼
  └── Réponse JSON enrichie
🟦 5. Architecture MLflow (Tracking + Registry)
MLflow est utilisé pour :

suivre les entraînements

stocker les artefacts

versionner les modèles

servir le modèle Production

Schéma MLflow
Code
Entraînement (train.py)
        │
        ▼
mlflow.log_params()
mlflow.log_metrics()
mlflow.log_artifacts()
mlflow.sklearn.log_model()
        │
        ▼
      Run MLflow
        │
        ▼
   Model Registry
        │
        ├── Version 1
        ├── Version 2
        ├── Version 3
        └── Production  ← utilisé par l’API
🟩 6. Architecture du service de prédiction
Le cœur métier se trouve dans :

Code
src/api/prediction_service.py
Rôle du service :
charger le modèle (run_id ou Production)

vectoriser le texte

prédire le code

décoder le label métier

mesurer le temps d’inférence

construire la réponse JSON

Schéma du service
Code
Entrée utilisateur
      │
      ▼
Chargement modèle MLflow
      │
      ▼
Pipeline sklearn (TF-IDF + LinearSVC)
      │
      ▼
prediction_code
      │
      ▼
Mapping CSV → label métier
      │
      ▼
Construction réponse JSON
🟧 7. Architecture du mode hybride (run_id / Production)
Le mode hybride est une fonctionnalité clé de la V2.

Schéma :
Code
Si run_id fourni :
    → Charger modèle du run MLflow

Si run_id = null :
    → Charger modèle Production du Model Registry
Avantages :
tests A/B

reproductibilité

debug d’un modèle spécifique

stabilité en production

🟦 8. Architecture des tests automatisés
Les tests sont organisés en 3 niveaux :

Code
tests/
│
├── test_api_unit.py        ← Tests unitaires
├── test_api_integration.py ← Tests API ↔ MLflow
└── test_api_e2e.py         ← Tests end-to-end
Schéma des tests
Code
Unit tests
    │
    ▼
Validation Pydantic
Sécurité token
Erreurs 401/422

Integration tests
    │
    ▼
API ↔ MLflow
Mapping métier
Structure JSON

E2E tests
    │
    ▼
Parcours complet utilisateur
Cohérence API / Swagger
🟩 9. Architecture du mapping métier
Dans la V2, le mapping est chargé depuis un CSV :

Code
Y_train_encode.csv
Schéma :
Code
prediction_code
      │
      ▼
Mapping CSV
      │
      ▼
label métier
Pourquoi CSV ?
plus simple

plus portable

plus rapide

plus facile à maintenir

🟧 10. Architecture complète (vue finale)
Voici la vue complète, intégrant API + MLflow + modèle + mapping :

Code
Client
  │
  ├── POST /predict
  │
  ▼
FastAPI (app.py)
  │
  ▼
Validation Pydantic (schemas.py)
  │
  ▼
prediction_service.py
  │
  ▼
utils.load_model()
  │
  ├── run_id ? → MLflow run
  └── sinon → Model Registry (Production)
  │
  ▼
Pipeline sklearn (TF-IDF + LinearSVC)
  │
  ▼
prediction_code
  │
  ▼
Mapping CSV → label métier
  │
  ▼
Construction réponse JSON
  │
  ▼
Réponse enrichie
🟦 11. Conclusion
L’architecture V2 est :

simple

robuste

professionnelle

alignée MLOps

compréhensible pour une équipe débutante

prête pour la production

Elle sépare clairement :

API

logique métier

modèle

MLflow

mapping métier

tests

Ce document permet à n’importe quelle personne de comprendre comment tout fonctionne, sans lire le code.

